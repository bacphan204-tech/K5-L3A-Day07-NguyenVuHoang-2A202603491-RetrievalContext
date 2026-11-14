# Code Day 7

| File | Công dụng |
|---|---|
| `prepare_day6.py` | Nhập và kiểm chứng chunk B, nguồn và metadata từ Day 6 |
| `dense_retrieval.py` | E5 local + bản sao Chroma `economics_b` |
| `lexical_retrieval.py`, `hybrid_retrieval.py` | BM25 và hybrid bằng RRF |
| `retrieval_improvements.py` | Dọn query phạm vi chương và sentence rerank |
| `agent_retriever.py` | Adapter retrieval dùng chung cho agent và batch |
| `llm_client.py`, `book_agent.py` | OpenAI Responses, tool loop, context, citation/abstention |
| `benchmark.py`, `retrieval_metrics.py`, `agent_evaluation.py` | Tách nhãn khỏi input; chấm retrieval và tổng hợp dữ liệu đánh giá |

Các lệnh chạy đặt trong `scripts/`; xem [README chính](../README.md). Model/khóa test không được đổi để chỉnh theo kết quả test đã xem. Nhãn nội dung có AI hỗ trợ, xem báo cáo cá nhân và `reviews.json`.
