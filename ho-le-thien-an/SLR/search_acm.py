"""Collect public ACM search metadata and register unscreened candidates.

Standard library only. HTTP 403 is reported, never worked around. When direct
HTTP is unavailable, import a saved search page or a browser DOM snapshot.
"""
import argparse
import csv
import hashlib
import json
import re
import sys
import tempfile
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEFAULT_SNAPSHOT = HERE / "raw/acm_2026-10-09_page1.json"
SHARED_FIELDS = "record_id member database title authors year doi url decision reason dedup_key notes".split()
PERSONAL_FIELDS = "paper_id title authors year doi_or_url decision reason notes".split()
LOG_FIELDS = "database query date raw_hits screened candidate included notes".split()


def normalize_doi(value):
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value.strip(), flags=re.I)
    return re.sub(r"^doi:\s*", "", value, flags=re.I).lower()


def title_key(title):
    return " ".join(re.findall(r"\w+", unicodedata.normalize("NFKC", title).casefold()))


def record_keys(row):
    value = row.get("doi") or row.get("doi_or_url") or ""
    doi = normalize_doi(value)
    keys = set()
    if re.fullmatch(r"10\.\d{4,9}/\S+", doi):
        keys.add("doi:" + doi)
    if row.get("title") and row.get("year"):
        keys.add("title:" + title_key(row["title"]) + ":" + str(row["year"]))
    return keys


def read_csv(file):
    if not file.exists():
        return [], None
    with file.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        if any(None in row or any(v is None for v in row.values()) for row in rows):
            raise ValueError(f"Malformed CSV: {file}")
        return rows, reader.fieldnames


def append_csv(file, fields, rows):
    if not rows:
        return
    _, existing_fields = read_csv(file)
    if existing_fields and existing_fields != fields:
        raise ValueError(f"Unexpected CSV columns: {file}")
    file.parent.mkdir(parents=True, exist_ok=True)
    has_content = file.exists() and file.stat().st_size > 0
    needs_newline = has_content and not file.read_bytes().endswith((b"\n", b"\r"))
    with file.open("a", encoding="utf-8", newline="") as stream:
        if needs_newline:
            stream.write("\n")
        writer = csv.DictWriter(stream, fieldnames=fields)
        if not has_content:
            writer.writeheader()
        writer.writerows(rows)


class Node:
    def __init__(self, tag="", attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

    def text(self):
        return "".join(c.text() if isinstance(c, Node) else c for c in self.children)

    def find(self, predicate):
        found = [self] if predicate(self) else []
        for child in self.children:
            if isinstance(child, Node):
                found.extend(child.find(predicate))
        return found

    def has_class(self, name):
        return name in self.attrs.get("class", "").split()


class SearchParser(HTMLParser):
    VOID = set("area base br col embed hr img input link meta param source track wbr".split())

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        if not any(n.tag in {"script", "style"} for n in self.stack):
            self.stack[-1].children.append(data)


def parse_search_html(html, source_url, retrieved_date):
    parser = SearchParser()
    parser.feed(html)
    root = parser.root
    query = urllib.parse.parse_qs(urllib.parse.urlparse(source_url).query).get("AllField", [""])[0]
    if not query:
        raise ValueError("Source URL must contain the actual ACM AllField query.")
    count = re.search(r"([\d,]+)\s+Results\s+for\s*:", root.text(), re.I)
    if not count:
        raise ValueError("No ACM result count found; the page may be a login or access-check page.")
    records = []
    for card in root.find(lambda n: n.has_class("issue-item--search")):
        titles = card.find(lambda n: n.has_class("issue-item__title"))
        links = titles[0].find(lambda n: n.tag == "a") if titles else []
        dois = card.find(lambda n: n.has_class("issue-item__doi"))
        dates = card.find(lambda n: n.has_class("bookPubDate"))
        authors = card.find(lambda n: n.attrs.get("aria-label") == "authors")
        if not links or not dois:
            raise ValueError("An ACM result lacks title/DOI; inspect the saved page before importing.")
        records.append({
            "rank": len(records) + 1, "title": " ".join(titles[0].text().split()),
            "authors": [" ".join(a.text().split()) for a in authors[0].find(lambda n: n.tag == "a")] if authors else [],
            "display_date": dates[0].text().strip() if dates else "",
            "doi": normalize_doi(dois[0].text()),
            "url": urllib.parse.urljoin(source_url, links[0].attrs["href"]),
        })
    return {"schema_version": 1, "database": "ACM Digital Library", "capture_method": "saved_search_html",
            "query": query, "search_url": source_url, "raw_hits": int(count[1].replace(",", "")),
            "retrieved_date": retrieved_date, "page": 1, "records": records}


def validate_snapshot(snapshot):
    if snapshot.get("database") != "ACM Digital Library":
        raise ValueError("Snapshot database must be ACM Digital Library.")
    parsed = urllib.parse.urlparse(snapshot.get("search_url", ""))
    if parsed.scheme != "https" or parsed.hostname != "dl.acm.org":
        raise ValueError("Snapshot must retain an HTTPS ACM search URL.")
    actual_query = urllib.parse.parse_qs(parsed.query).get("AllField", [""])[0]
    if not actual_query or actual_query != snapshot.get("query"):
        raise ValueError("Stored query does not match the source URL.")
    datetime.strptime(snapshot["retrieved_date"], "%Y-%m-%d")
    if not isinstance(snapshot.get("raw_hits"), int) or snapshot["raw_hits"] < len(snapshot["records"]):
        raise ValueError("Invalid raw hit count.")
    for row in snapshot["records"]:
        if not row.get("title") or not re.fullmatch(r"10\.\d{4,9}/\S+", normalize_doi(row.get("doi", ""))):
            raise ValueError("Each result must have a title and DOI.")
        if not re.search(r"\b(?:19|20)\d{2}\b", row.get("display_date", "")):
            raise ValueError("Missing display year; do not invent it.")


def save_candidates(snapshot, root):
    validate_snapshot(snapshot)
    folder = root / "ho-le-thien-an/SLR"
    shared_path, personal_path = root / "RQ_01_all_records.csv", folder / "candidate_papers.csv"
    shared, _ = read_csv(shared_path)
    personal, _ = read_csv(personal_path)
    shared_keys = set().union(*(record_keys(r) for r in shared))
    personal_keys = set().union(*(record_keys(r) for r in personal))
    known = []
    for file in root.glob("*/SLR/candidate_papers.csv"):
        if file == personal_path:
            continue
        for row in read_csv(file)[0]:
            known.append((record_keys(row), str(file.relative_to(root)), row.get("paper_id", "")))
    run_id = hashlib.sha256(json.dumps(snapshot, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]
    ids = [r.get("record_id", r.get("paper_id", "")) for r in shared + personal]
    next_id = max([int(m[1]) for value in ids if (m := re.fullmatch(r"AN-SLR-(\d+)", value))] or [0]) + 1
    new_shared, new_personal, overlaps, seen = [], [], [], set()
    for item in snapshot["records"]:
        doi = normalize_doi(item["doi"])
        year = re.search(r"\b(?:19|20)\d{2}\b", item["display_date"])[0]
        keys = record_keys({"doi": doi, "title": item["title"], "year": year})
        if seen & keys:
            continue
        seen.update(keys)
        matches = [{"file": file, "paper_id": pid} for other, file, pid in known if keys & other]
        if matches:
            overlaps.append({"doi": doi, "matches": matches})
        note = (f"run={run_id}; {snapshot['capture_method']}; page={snapshot.get('page', 1)}; "
                f"rank={item['rank']}; date={snapshot['retrieved_date']}; unscreened; "
                "authors as displayed (may be truncated); year from search display date")
        if matches:
            note += "; also in " + "; ".join(m["file"] + "#" + m["paper_id"] for m in matches)
        existing = next((r for r in personal + shared if keys & record_keys(r)), None)
        pid = (existing.get("paper_id") or existing.get("record_id")) if existing else f"AN-SLR-{next_id:03d}"
        if not existing:
            next_id += 1
        row = dict(zip(SHARED_FIELDS, [pid, "Hồ Lê Thiên An", "ACM Digital Library", item["title"],
                   "; ".join(item["authors"]), year, doi, item["url"], "candidate",
                   "Retrieved by query; title/abstract screening pending", "doi:" + doi, note]))
        if not keys & shared_keys:
            new_shared.append(row)
            shared_keys.update(keys)
        if not keys & personal_keys:
            new_personal.append(dict(zip(PERSONAL_FIELDS, [pid, row['title'], row['authors'], year,
                                "https://doi.org/" + doi, "candidate", row['reason'], note])))
            personal_keys.update(keys)
    # Each destination deduplicates independently: an interrupted run can be safely repeated.
    append_csv(personal_path, PERSONAL_FIELDS, new_personal)
    append_csv(shared_path, SHARED_FIELDS, new_shared)
    log_path = folder / "search_log.csv"
    if not any(f"run={run_id}" in row.get("notes", "") for row in read_csv(log_path)[0]):
        append_csv(log_path, LOG_FIELDS, [{"database": "ACM Digital Library", "query": snapshot["query"],
            "date": snapshot["retrieved_date"], "raw_hits": snapshot["raw_hits"], "screened": 0,
            "candidate": len({normalize_doi(r['doi']) for r in snapshot['records']}), "included": 0,
            "notes": f"run={run_id}; {snapshot['capture_method']}; collected={len(snapshot['records'])}; "
                     f"page={snapshot.get('page', 1)} only; candidates are unscreened retrieval records; "
                     f"cross-member overlaps={len(overlaps)}; source={snapshot['search_url']}"}])
    audit = folder / "raw" / f"dedup_{run_id}.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    if not audit.exists():
        audit.write_text(json.dumps({"run_id": run_id, "cross_member_overlaps": overlaps,
            "note": "An keeps source-specific records; the shared CSV keeps one row per DOI/title-year."},
            ensure_ascii=False, indent=2), encoding="utf-8")
    return {"collected": len(snapshot["records"]), "new_shared": len(new_shared),
            "new_personal": len(new_personal), "cross_member_overlaps": len(overlaps), "run_id": run_id}


def crawl(query):
    url = "https://dl.acm.org/action/doSearch?" + urllib.parse.urlencode({"AllField": query})
    request = urllib.request.Request(url, headers={"User-Agent": "SHA256-SLR-metadata/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        if error.code in {401, 403, 429}:
            raise RuntimeError(f"ACM returned HTTP {error.code}. Open the search in your browser, save the "
                               "page as HTML and use --html with --source-url and --date. No records written.") from error
        raise
    date = datetime.now(timezone(timedelta(hours=7))).date().isoformat()
    snapshot = parse_search_html(html, url, date)
    snapshot["capture_method"] = "python_http"
    return snapshot, html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true", help="Replay the saved real ACM sample in a temporary folder")
    mode.add_argument("--crawl", action="store_true", help="Fetch the first public ACM results page over HTTP")
    mode.add_argument("--snapshot", type=Path, help="Import an ACM browser snapshot JSON")
    mode.add_argument("--html", type=Path, help="Import an ACM results page saved from a browser")
    parser.add_argument("--query", help="Actual query, required for --crawl")
    parser.add_argument("--source-url", help="Original search URL, required for --html")
    parser.add_argument("--date", help="Date the HTML was retrieved, YYYY-MM-DD")
    args = parser.parse_args()
    if args.demo:
        snapshot = json.loads(DEFAULT_SNAPSHOT.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory(prefix=".acm-demo-", dir=HERE) as directory:
            print(f"Replay of REAL saved ACM metadata: {snapshot['raw_hits']} hits; page 1 sample only.")
            first = save_candidates(snapshot, Path(directory))
            print(f"First import: {first['new_shared']} candidates added; screened=0; included=0.")
            second = save_candidates(snapshot, Path(directory))
            print(f"Second import: {second['new_shared']} new rows (duplicates skipped).")
            assert first['new_shared'] > 0 and second['new_shared'] == 0
            print("Demo passed. Research CSV files were not modified.")
        return
    if args.crawl:
        if not args.query:
            parser.error("--crawl requires --query")
        snapshot, html = crawl(args.query)
    elif args.html:
        if not args.source_url or not args.date:
            parser.error("--html requires --source-url and --date")
        html = args.html.read_text(encoding="utf-8-sig")
        snapshot = parse_search_html(html, args.source_url, args.date)
    else:
        html = None
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8-sig"))
    validate_snapshot(snapshot)
    raw = HERE / "raw"
    raw.mkdir(exist_ok=True)
    digest = hashlib.sha256(json.dumps(snapshot, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]
    (raw / f"capture_{digest}.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    if html is not None:
        (raw / f"capture_{digest}.html").write_text(html, encoding="utf-8")
    result = save_candidates(snapshot, ROOT)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("Saved as candidate only. Human screening still pending.")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
