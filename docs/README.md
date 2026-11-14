# Đối chiếu yêu cầu và minh chứng bài nộp

Đối chiếu theo [GUIDE](../GUIDE.md), [BENCHMARK](../BENCHMARK.md), [RUBRIC](../RUBRIC.md) và [SUBMISSION](../SUBMISSION.md). Phạm vi là phần cơ bản, tối đa 85 điểm; không tự chấm số điểm được nhận.

| Hạng mục | Yêu cầu cần có | Minh chứng hiện có | Nhận xét |
|---|---|---|---|
| Dữ liệu và benchmark (13 điểm) | Kết nối Day 6, model/vector store thật; tối thiểu 15+2 dev, 5+2 test; nguồn và evidence | `data/day6/`, `benchmark/`, phần 1–2 báo cáo | Đủ số lượng; giữ 52 trang, 183 chunk, E5 384 chiều, Chroma. Nhãn do AI hỗ trợ, chưa xác nhận độc lập của học viên. |
| Retrieval (17 điểm) | Ít nhất ba phương pháp, gồm dense Day 6; cấu hình, nguồn, rank/score và lỗi | `src/`, `results/part05/dev-20261114T090138Z-f9b815/` | Dense, BM25, RRF hybrid; cùng corpus/query/filter. BM25 kém do khác ngôn ngữ, kết quả thấp vẫn giữ. |
| Agent và context (17 điểm) | Model thật gọi tool, điều kiện dừng, trace, context/citation và thiếu evidence | `src/book_agent.py`, `results/part08/`, `results/final/test/` | OpenAI Responses; 3 search/4 model call; 5.000 ký tự. Chuẩn hóa định dạng có raw output và provenance; không bảo đảm semantic đúng mọi câu. |
| Đánh giá (17 điểm) | Hit@1/Hit@3, Context Evidence Rate, đọc câu trả lời/citation/abstention/tool use | `evaluation_summary.json`, `reviews.json`, `artifacts/*_review_decisions.json`, phần 5–6 báo cáo | Đã chấm 34 ca dev, 14 ca test; đủ 5 câu test có đáp án và 2 câu thiếu evidence cho mỗi cấu hình. Có strict và nhãn đối chiếu nguồn riêng. |
| Cải thiện (13 điểm) | Hai cấu hình có giả thuyết, ít nhất hai lỗi dev; chọn dev trước test; chi phí/thời gian | `artifacts/dev_improvement_plan.json`, `results/part06/`, `benchmark/frozen.json` | Cleanup và sentence rerank, before/after q03/q12, paired changes. Quy tắc chọn cụ thể ghi sau thăm dò dev nhưng trước test, đã công bố giới hạn. |
| Tái lập và báo cáo (8 điểm) | Code, cách chạy, model/dữ liệu, kết luận và giới hạn | [README](../README.md), requirements, [báo cáo cá nhân](../report/individual/2A202603491_NguyenVuHoang.md) | Có phụ thuộc Day 6 để tái tạo model/index; không nộp venv/model và key. Cần kiểm tra quyền xem repo khi nộp. |

## Những điểm không được hiểu nhầm

- `48/48 unit tests` và `check_submission.py: PASS` xác nhận code/cấu trúc/minh chứng, không xác nhận mọi câu trả lời đúng hoặc chắc chắn nhận đủ 85 điểm.
- Tập test chỉ 7 câu. Nhãn do Codex AI đối chiếu text nguồn, cùng AI tham gia triển khai; `student_confirmed=false` được giữ đúng thực tế.
- Ca demo `results/part07/20261114T100017Z-02e9bc/trace.json` trả lời lệch câu hỏi dù `answered`. Báo cáo đã ghi nhận, không chỉnh pipeline sau test.
- Không làm thử thách 100 trang, không yêu cầu 15 điểm bonus.
- Học viên cần đọc hiểu báo cáo, xác nhận các nhãn đã tự kiểm tra, đảm bảo giảng viên truy cập được repo và nộp link theo thông báo lớp. Việc push GitHub không tự gửi bài cho giảng viên.

## Kiểm tra nhanh

```powershell
python -X utf8 -m unittest discover -s tests -v
python -X utf8 scripts/check_submission.py
```

Hai lệnh không gọi API. Gói zip tạo bằng `python -X utf8 scripts/package_submission.py`; key `.env` và runtime `.local`/venv không được đóng gói.

## Dọn thư mục

Giữ toàn bộ file của bộ đề ban đầu. Các tài liệu hướng dẫn PART01–PART08, bản sao đề, checklist trùng, script sinh lại báo cáo tự động và lượt chạy tạm/trùng đã được bỏ. Giữ lượt benchmark dùng trong báo cáo, lượt tạo sentence bank đầu tiên, dev gốc/bản revalidated được dùng để chọn cấu hình, toàn bộ test và ca demo lỗi cần minh chứng. Runtime local vẫn giữ để tiếp tục chạy nhưng không nằm trong gói nộp.
