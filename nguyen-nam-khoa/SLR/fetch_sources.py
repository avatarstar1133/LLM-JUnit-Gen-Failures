"""Archive public retrieval attempts for the 2026-10-09 SLR screening."""
import concurrent.futures
import json
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
import sys
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "sources"
OUT.mkdir(exist_ok=True)
QUERY = ('("unit test generation" OR "JUnit test suite" OR HumanEval) AND '
         '(ChatGPT OR Gemini OR "compiler-feedback repair" OR "structured prompting") AND '
         '(compilability OR executability OR "build success rate" OR "test execution rate")')

def fetch(item):
    key, url = item
    record = {"key": key, "url": url, "date": "2026-10-09", "timezone": "Asia/Saigon"}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (SLR research; public sources)"})
        with urllib.request.urlopen(request, timeout=25) as response:
            body = response.read()
            ctype = response.headers.get("Content-Type", "")
            extension = ".pdf" if body.startswith(b"%PDF") else ".json" if "json" in ctype else ".html"
            target = OUT / (key + extension)
            target.write_bytes(body)
            record.update(status=response.status, final_url=response.url, bytes=len(body), file=target.name, content_type=ctype)
            if extension == ".json":
                record["reported_total"] = json.loads(body).get("total")
    except Exception as exc:
        record.update(status="ERROR", error=str(exc))
    return record

items = [
    ("semantic_scholar_shared_query", "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode({"query": QUERY, "limit": 100, "fields": "title,authors,year,url,externalIds,openAccessPdf,abstract"})),
    ("google_scholar_shared_query", "https://scholar.google.com/scholar?" + urllib.parse.urlencode({"q": QUERY, "num": 20})),
    ("testart_v6", "https://arxiv.org/html/2408.03095v6"),
    ("meta_v1", "https://arxiv.org/html/2402.09171v1"),
    ("yate_v1", "https://arxiv.org/html/2507.18316v1"),
    ("tcs_v1", "https://arxiv.org/html/2609.03955v1"),
    ("oracle_audit_v1", "https://arxiv.org/html/2608.19626v1"),
    ("llm2alloy_v1", "https://arxiv.org/html/2607.18555v1"),
    ("business_oracles_v1", "https://arxiv.org/html/2607.10277v1"),
    ("chattester_v3", "https://arxiv.org/html/2305.04207v3"),
    ("chatunitest", "https://arxiv.org/html/2305.04764"),
    ("chaining_ieee", "https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11269709"),
    ("repair_ieee", "https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11527996"),
    ("llm_test_publisher", "https://doi.org/10.63090/IJITRS/3139.3209.0022"),
    ("failmapper_github", "https://api.github.com/repos/nuwaLab/FailMapper/git/trees/main?recursive=1"),
]
if "--supplement" in sys.argv:
    items = [
        ("chaining_fulltext", "https://ieeexplore.ieee.org/ielx8/6287639/10820123/11269709.pdf"),
        ("llm_test_fulltext", "https://www.eduresearchjournal.com/index.php/ijitrs/article/download/642/616/3468"),
    ]
    previous = json.loads((OUT / "retrieval_log.json").read_text(encoding="utf-8"))
else:
    previous = []
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    records = list(pool.map(fetch, items))
(OUT / "retrieval_log.json").write_text(json.dumps(previous + records, ensure_ascii=False, indent=2), encoding="utf-8")

class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.ignore = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.ignore += 1
        if tag in ("p", "h1", "h2", "h3", "h4", "tr", "section"):
            self.parts.append("\n")
        if tag in ("td", "th"):
            self.parts.append(" | ")
    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.ignore = max(0, self.ignore - 1)
    def handle_data(self, data):
        if not self.ignore:
            self.parts.append(data)

for source in OUT.glob("*.html"):
    parser = TextParser()
    parser.feed(source.read_text(encoding="utf-8", errors="replace"))
    text = "\n".join(" ".join(line.split()) for line in "".join(parser.parts).splitlines() if line.strip())
    source.with_suffix(".txt").write_text(text, encoding="utf-8")
for source in OUT.glob("*.pdf"):
    from pypdf import PdfReader
    reader = PdfReader(source)
    source.with_suffix(".txt").write_text("\n\n".join(f"PAGE {i + 1}\n{page.extract_text()}" for i, page in enumerate(reader.pages)), encoding="utf-8")
print(json.dumps(records, ensure_ascii=False, indent=2))
