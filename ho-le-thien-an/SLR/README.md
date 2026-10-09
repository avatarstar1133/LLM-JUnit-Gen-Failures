# Hồ Lê Thiên An – SLR
Primary source: **ACM Digital Library**.
Use the shared query and IC/EC from `team-synthesis/`.
Record every search session in `search_log.csv` and candidate papers in `candidate_papers.csv`.

## Python metadata tool

Run `demo_acm.cmd` for a short replay of the saved real ACM sample. See
[demo instructions](manual_acm_demo.md) for commands and provenance.

The 2026-10-09 collection contains 20 records from the first page of 611 ACM
search hits. Direct Python HTTP returned 403, so browser-rendered public metadata
was captured and imported by `search_acm.py`. All records remain unscreened
`candidate` entries. The authors field may be truncated by the search page.
