# Dev retrieval — original queries

| Method | Hit@1 | Evidence Hit@3 | Errors | Median query (ms) |
|---|---:|---:|---:|---:|
| dense | 2/15 (13.33%) | 6/15 (40.00%) | 0 | 48.32 |
| bm25 | 1/15 (6.67%) | 1/15 (6.67%) | 0 | 0.58 |
| hybrid | 3/15 (20.00%) | 6/15 (40.00%) | 0 | 48.90 |

15 answerable cases form the retrieval denominator; 2 unanswerable cases are traced separately.
Errors count as misses in the fixed denominator and are reported explicitly.
No context/agent/citation/abstention metrics have been measured. No test inputs or labels were loaded.
See summary.json for configuration, costs, timing limitations and trace provenance.
