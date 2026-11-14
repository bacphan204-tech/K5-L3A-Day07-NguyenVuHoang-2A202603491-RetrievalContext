# Day 7 — Agentic RAG trên sách kinh tế

**Nguyễn Vũ Hoàng · MSSV 2A202603491 · L3A**

Tiếp nối [Day 6](https://github.com/bacphan204-tech/K5-L3A-Day06-NguyenVuHoang-2A202603491-DataIngestionEngineering): 52 trang nội dung OpenStax, E5 đa ngữ + Chroma, dense/BM25/hybrid, hai thí nghiệm cải thiện và agent OpenAI có citation/abstention.

[Báo cáo chính](report/individual/2A202603491_NguyenVuHoang.md) · [Kết quả test](results/final/test/evaluation_summary.json) · [Khóa cấu hình](benchmark/frozen.json) · [Đối chiếu yêu cầu nộp](docs/README.md)

## Kết quả đã lưu

| Chỉ số | Dense baseline | Cấu hình chọn: cleanup + sentence rerank |
|---|---:|---:|
| Dev grounded answer trung bình /2 | 1,47 | 1,73 |
| Test grounded answer trung bình /2 | 1,40 | 2,00 |
| Test context đủ evidence (đối chiếu nguồn) | 3/5 | 5/5 |
| Test citation hỗ trợ nội dung | 4/6 | 7/7 |
| Test từ chối đúng | 2/2 | 2/2 |

Nhãn phần cơ bản do **Codex AI đọc và đối chiếu nguồn**, chưa có xác nhận độc lập của học viên. Test cơ bản chỉ 7 câu, cùng hai chương với dev, không suy rộng ra mọi câu hỏi kinh tế. Phần bonus 120 trang đã được thử riêng: test khóa v1 đạt **23/30 (76,7%)**, thấp hơn ngưỡng 90%. Bản v1 được giữ nguyên; pipeline sau đó được điều chỉnh trên dev và các ca lỗi cũ chỉ dùng để chẩn đoán, không tính là điểm holdout. Chưa có test mới độc lập nên chưa thể xác nhận đạt bonus. Xem [advanced/README.md](advanced/README.md) và [báo cáo test v1](advanced/reports/test-vision-evaluation.json).

## Chạy nhanh tại gốc Day 7

```powershell
python -X utf8 -m unittest discover -s tests -v
python -X utf8 scripts/prepare_benchmark.py --check-only
python -X utf8 scripts/final_evaluation.py verify-lock
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\ask_agent.ps1 -Question "Ai cung ứng lao động?" -Chapter 4
```

Agent đọc key từ `.env` và gọi API có phí. Không gửi key vào chat/Git. Model mặc định `gpt-5.4-mini-2026-03-17`; embedding local `intfloat/multilingual-e5-small`, 384 chiều. `Bypass` chỉ áp dụng tiến trình PowerShell đó.

## Tái tạo trên máy mới

1. Clone repo Day 6 liên kết ở trên và repo Day 7 vào hai thư mục cùng cấp, giữ tên hiện tại. Từ gốc Day 6 chạy `starter/scripts/run_all.ps1 -Install` theo README Day 6 để tạo venv, tải model đã pin và xây Chroma. Không cần API key cho Day 6.
2. Từ gốc Day 7 chạy `python -X utf8 src/prepare_day6.py`. Kỳ vọng 183 chunk B, 52 trang. Lần retrieval đầu tạo bản sao Chroma Day 7. Model, index và venv không nằm trong gói nộp.
3. Nếu chưa có `.env`, sao chép mẫu và nhập key riêng của người chạy:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\ask_agent.ps1 -CheckConfig
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\ask_agent.ps1 -CheckApi
```

`-CheckApi` có một lượt API nhỏ tính phí. `requirements.txt` ghi thư viện lõi, `requirements-lock.txt` lưu môi trường Day 6 đã dùng (Windows/Python 3.14.6). Wrapper tái sử dụng venv Day 6 để tránh cài trùng; trên Linux hoặc khi đổi vị trí cần dùng CLI Python/môi trường và đường dẫn tương ứng. Artifact đã lưu đọc được không cần key/API.

Khóa dùng byte hash; `.gitattributes` giữ nguyên bytes qua Git checkout để tránh đổi LF/CRLF. Corpus tái tạo trên nền tảng khác có thể khác bytes/newline: cần đối chiếu như kiểm tra tái lập riêng, không ghi đè khóa gốc hay gọi test đã xem là holdout mới.

## Thí nghiệm và đánh giá

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\compare_retrieval.ps1 -Question "Ai cung ứng lao động?" -Chapter 4
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\benchmark_dev.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\experiment_dev.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\agent_dev.ps1
python -X utf8 scripts/summarize_agent_dev.py --run results/final/test
```

Ba lệnh dev ghi lượt mới, không ghi đè lượt trước; agent dev có phí. Không tạo lại benchmark sau khóa; chỉ dùng `prepare_benchmark.py --check-only`. `final_evaluation.py test` chạy bằng venv Day 6, kiểm tra khóa và bỏ qua trace đã có. Không chỉnh theo test; nghiên cứu mới cần bộ test mới.

- `benchmark/`: 17 dev, 7 test, gold/inputs tách biệt, absence review và khóa.
- `artifacts/`: kế hoạch cải thiện, nhãn AI từng câu có lý do.
- `results/part05/`, `part06/`: ba phương pháp và hai cải thiện trên dev.
- `results/part08/`: 34 ca agent dev, bản gốc lỗi và bản revalidated offline riêng.
- `results/final/test/`: 14 trace agent test, retrieval query gốc, context/đáp án/citation/chi phí/nhãn.
- `results/final/source_verification.json`: kiểm tra PDF text; không phải kiểm tra layout/OCR.
- `docs/README.md`: đối chiếu yêu cầu và minh chứng; `report/individual/`: báo cáo cá nhân. Các file đề bài gốc vẫn giữ ở thư mục gốc.

Citation ID hợp lệ chưa bảo đảm đáp án grounded. Các lỗi vẫn giữ: dev q08 cite đoạn bưu chính cho inferior good; test dense q02 lẫn cầu/lượng cầu và q04 thiếu evidence về niềm tin trả nợ. Chuẩn hóa định dạng có raw decision và provenance, không thay thế chấm nghĩa.

Nguồn: OpenStax, Rice University, *Principles of Economics 3e*. Access for free at openstax.org. PDF trích, evidence và trace giữ attribution/CC BY-NC-SA 4.0 theo manifest. Thư viện/model có giấy phép riêng. Học viên cần đọc hiểu, xác nhận nhãn và đảm bảo giảng viên xem được repo; không nhận rằng học viên đã chấm độc lập khi chưa làm.
