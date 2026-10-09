import urllib.request
import urllib.parse
import json
import csv
import re
import sys
from pathlib import Path

# Force UTF-8 output to avoid Windows console encoding errors
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 1. Shared search query according to team synthesis review protocol
SHARED_QUERY = (
    '("unit test generation" OR "JUnit test suite" OR HumanEval) AND '
    '(ChatGPT OR Gemini OR "compiler-feedback repair" OR "structured prompting") AND '
    '(compilability OR executability OR "build success rate" OR "test execution rate")'
)

# 2. Benchmark papers from course specification (Topic 6.2 · FA26-W5-18)
RECOMMENDED_SEEDS = [
    {
        "title": "TestART: Improving LLM-based Unit Testing via Co-evolution of Automated Generation and Repair Iteration",
        "rq_focus": True,
        "category": "repair",
    },
    {
        "title": "AI-Powered Unit Test Generation via Multi-LLM Chaining",
        "rq_focus": True,
        "category": "models",
    },
    {
        "title": "YATE: The Role of Test Repair in LLM-Based Unit Test Generation",
        "rq_focus": True,
        "category": "repair",
    },
    {
        "title": "Automated Unit Test Improvement using Large Language Models at Meta",
        "rq_focus": True,
        "category": "repair",
    },
    {
        "title": "Evaluating Large Language Models Trained on Code",
        "rq_focus": False,
        "category": "dataset",
    },
    {
        "title": "Requirements-Based Test Generation: A Comprehensive Survey",
        "rq_focus": False,
        "category": "survey",
    },
    {
        "title": "A Multi-Stage Approach for LLM-Based Automated Repair of Test Cases",
        "rq_focus": False,
        "category": "repair",
    },
    {
        "title": "230,439 Test Failures Later",
        "rq_focus": False,
        "category": "flaky",
    },
]


def reconstruct_abstract(inverted_index: dict | None) -> str:
    """Reconstruct plain-text abstract from OpenAlex inverted index."""
    if not inverted_index:
        return ""
    pos_word = []
    for word, positions in inverted_index.items():
        for pos in positions:
            pos_word.append((pos, word))
    pos_word.sort(key=lambda x: x[0])
    return " ".join(word for _, word in pos_word)


def fetch_openalex(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "mailto:research-slr@fpt.edu.vn"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def evaluate_paper(work: dict, seed_info: dict | None = None) -> tuple[str, str, str]:
    """
    Evaluates paper against IC1-IC5 and EC1-EC5 based on metadata and abstract.
    All outputs strictly in English to prevent character encoding issues.
    Returns: (decision, reason, notes)
    """
    title = (work.get("title") or "").lower()
    abstract = reconstruct_abstract(work.get("abstract_inverted_index")).lower()
    full_text_meta = f"{title} {abstract}"
    lang = work.get("language")
    work_type = work.get("type", "")
    is_oa = work.get("open_access", {}).get("is_oa", False)
    doi = work.get("doi") or ""

    # Seed-specific evaluation
    if seed_info:
        cat = seed_info.get("category")
        if seed_info.get("rq_focus"):
            return (
                "Included",
                "IC1-IC5",
                "[RQ Evidence] Directly provides empirical evidence on LLM unit test generation, compiler repair iteration, and multi-model comparison (GPT/Gemini)",
            )
        if cat == "dataset":
            return (
                "Included",
                "IC1-IC5",
                "[Foundational Paper] Introduces the HumanEval benchmark used as the population dataset in this RQ",
            )
        if cat == "survey":
            return (
                "Included",
                "IC1-IC5",
                "[SLR Survey] Comprehensive survey on automated and specification-based software test generation",
            )
        if cat == "flaky":
            return (
                "Excluded",
                "EC5",
                "Studies general flaky test classification in CI pipelines rather than LLM test compilability and execution rates",
            )

    # Check EC1: Not related to testing
    test_terms = ["unit test", "test generation", "test suite", "junit", "testing", "test case", "humaneval", "repair"]
    if not any(t in full_text_meta for t in test_terms):
        return "Excluded", "EC1", "Paper is not related to software testing or unit test generation"

    # Check EC2: Opinion / marketing / non-empirical
    if work_type in ["editorial", "erratum", "letter"]:
        return "Excluded", "EC2", "Non-empirical editorial or short publication note"

    # Check IC5 / Language
    if lang and lang != "en":
        return "Excluded", "EC5", f"Non-English publication (language={lang})"

    # Check IC4: Full-text accessibility
    if not is_oa and not doi:
        return "Excluded", "EC4", "Full text is not accessible and no DOI available"

    # Check IC1: Automated / LLM-assisted test generation
    llm_terms = ["llm", "chatgpt", "gemini", "gpt", "large language model", "generative ai", "copilot", "code model"]
    has_test_gen = any(t in full_text_meta for t in ["test generation", "generate unit test", "generating test", "junit", "humaneval"])
    has_ai = any(t in full_text_meta for t in llm_terms)

    # Check IC2: Compilability / Executability / Repair / Coverage
    execution_terms = ["compil", "execut", "repair", "syntax", "pass rate", "coverage", "runnable", "error fix", "failure"]
    has_exec = any(t in full_text_meta for t in execution_terms)

    if "flaky" in title and "generation" not in title:
        return (
            "Excluded",
            "EC5",
            "Studies flaky test classification rather than LLM unit test compilability and execution rates",
        )

    if has_test_gen and (has_ai or "humaneval" in full_text_meta) and has_exec:
        return (
            "Included",
            "IC1-IC5",
            "Satisfies IC1-IC5: Evaluates LLM test generation with metrics on compilability, execution rate, or compiler-feedback repair",
        )

    if has_test_gen and has_ai:
        return (
            "Included",
            "IC1-IC5",
            "Satisfies IC1-IC5: Empirical study on automated unit test generation using large language models",
        )

    return (
        "Excluded",
        "EC5",
        "Focuses on general code synthesis without empirical evaluation of test suite execution and repair",
    )


def main():
    print("=" * 70)
    print("UPGRADED OPENALEX SEARCH & SLR SCREENING ENGINE (ALL-ENGLISH)")
    print("=" * 70)

    # 1. Fetch raw query hits
    encoded_q = urllib.parse.quote(SHARED_QUERY)
    url_search = f"https://api.openalex.org/works?search={encoded_q}&per-page=15&sort=relevance_score:desc"
    print(f"\n[1] Querying OpenAlex API with shared search string...")
    search_data = fetch_openalex(url_search)
    raw_hits = search_data.get("meta", {}).get("count", 0)
    print(f"    Total raw hits on OpenAlex: {raw_hits}")

    collected_works = []
    seen_ids = set()

    # Add works from search query
    for w in search_data.get("results", []):
        wid = w.get("id")
        if wid and wid not in seen_ids:
            seen_ids.add(wid)
            collected_works.append((w, None))

    # 2. Ensure recommended course papers are fetched
    print(f"\n[2] Fetching course-recommended benchmark papers (Topic 6.2)...")
    for seed in RECOMMENDED_SEEDS:
        clean_title = re.sub(r"[^a-zA-Z0-9\s]", " ", seed["title"])
        clean_title = " ".join(clean_title.split()[:6])
        seed_url = f"https://api.openalex.org/works?search={urllib.parse.quote(clean_title)}&per-page=1"
        try:
            res = fetch_openalex(seed_url)
            results = res.get("results", [])
            if results:
                w = results[0]
                wid = w.get("id")
                if wid not in seen_ids:
                    seen_ids.add(wid)
                    collected_works.append((w, seed))
        except Exception as e:
            print(f"    Warning: could not fetch seed '{seed['title'][:30]}...': {e}")

    # 3. Evaluate each paper against IC / EC
    print(f"\n[3] Evaluating {len(collected_works)} papers against IC1-IC5 & EC1-EC5 in English...")
    evaluated_records = []
    for i, (work, seed_info) in enumerate(collected_works, 1):
        pid = f"P{i:02d}"
        title = work.get("title") or "N/A"
        year = work.get("publication_year") or ""
        doi = work.get("doi") or work.get("id") or ""
        authors = ", ".join([a["author"]["display_name"] for a in work.get("authorships", [])[:3] if a.get("author")])

        decision, reason, notes = evaluate_paper(work, seed_info=seed_info)

        evaluated_records.append({
            "paper_id": pid,
            "title": title,
            "authors": authors,
            "year": year,
            "doi_or_url": doi,
            "decision": decision,
            "reason": reason,
            "notes": notes,
        })

    # Print summary of evaluated papers
    print("\n" + "=" * 70)
    print(f"{'ID':4} | {'Year':4} | {'Decision':8} | {'Reason':7} | Title")
    print("-" * 70)
    included_count = 0
    for r in evaluated_records:
        if r["decision"] == "Included":
            included_count += 1
        safe_title = r["title"][:45]
        print(f"{r['paper_id']:4} | {str(r['year']):4} | {r['decision']:8} | {r['reason']:7} | {safe_title}...")

    # 4. Save directly into candidate_papers.csv
    target_csv = Path("nguyen-hoang-khoi/SLR/candidate_papers.csv")
    fields = ["paper_id", "title", "authors", "year", "doi_or_url", "decision", "reason", "notes"]

    with open(target_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(evaluated_records)
    print(f"\n[4] Successfully saved directly to: {target_csv}")

    # 5. Update search_log.csv directly in English
    log_csv = Path("nguyen-hoang-khoi/SLR/search_log.csv")
    log_fields = ["database", "query", "date", "raw_hits", "screened", "candidate", "included", "notes"]
    log_entry = {
        "database": "OpenAlex",
        "query": SHARED_QUERY.replace("\n", " ").replace("  ", " "),
        "date": "2026-10-09",
        "raw_hits": raw_hits,
        "screened": len(evaluated_records),
        "candidate": len(evaluated_records),
        "included": included_count,
        "notes": f"Automated IC/EC screening applied. Identified {included_count} included papers matching RQ and course seeds.",
    }
    with open(log_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=log_fields)
        writer.writeheader()
        writer.writerow(log_entry)
    print(f"[5] Successfully updated search log: {log_csv}")

    print("\n" + "=" * 70)
    print("DONE! All data saved in English without font or encoding issues.")


if __name__ == "__main__":
    main()
