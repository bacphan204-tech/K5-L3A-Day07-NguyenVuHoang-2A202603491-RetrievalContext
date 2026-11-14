# Dev retrieval improvement experiments

| Configuration | Hit@1 | Evidence Hit@3 | Errors | Median query ms |
|---|---:|---:|---:|---:|
| dense_original | 2/15 (13.33%) | 6/15 (40.00%) | 0 | 25.63 |
| clean_scope_dense | 3/15 (20.00%) | 7/15 (46.67%) | 0 | 25.42 |
| clean_scope_sentence_rerank | 7/15 (46.67%) | 9/15 (60.00%) | 0 | 46.54 |

Sentence embedding setup: {"unique_sentences": 1182, "cache_used": false, "setup_seconds": 13.204623500001617, "cache_path": "C:\\Users\\VU-HOANG-DZ\\Downloads\\K5-L3A-Day07-NguyenVuHoang-2A202603491-RetrievalContext\\.local\\e5_sentence_bank.json", "new_document_embeddings": 1182}

No test data loaded. No context/agent metrics or final configuration selected.
