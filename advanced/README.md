# Thử nghiệm bonus riêng

Phần cơ bản được giữ nguyên. Corpus nâng cao là **120 trang trích có chủ đích** từ OpenStax *Principles of Economics 3e*, gồm chương 1–5 và các trang sau có nội dung hữu ích về hệ thống tài chính. Đây là tuyển tập trang do học viên biên soạn, không tự nhận là bản sách đầy đủ hay một ấn phẩm độc lập. Mapping từng trang về số trang PDF gốc được giữ trong manifest.

Nguồn, giấy phép, hash, thống kê index và giới hạn ở `data/advanced/manifest.json`. `prepare.py` trích xuất text của toàn bộ 120 trang; ảnh trang gốc được giữ để retrieval vision render theo yêu cầu. Không có trang nào thiếu text index. Bảng, sơ đồ và biểu đồ được kiểm tra trực tiếp trên PDF gốc; hệ thống không xem caption OCR là gold.

## Tái lập

### Trạng thái lần thử đầu

Test v1 đã chạy đủ 30 câu và được đối chiếu với PDF: **23/30 (76,7%)**, dưới ngưỡng 90% (cần ít nhất 27/30); có 1 lỗi hệ thống. Kết quả chi tiết ở `reports/test-vision-evaluation.json`. V1 và trace gốc được giữ nguyên. Pipeline chỉnh sửa sau đó được thử trên dev và các ca test đã biết chỉ dùng để chẩn đoán, không tính là holdout hay điểm chính thức. Chưa khóa/chạy/chấm test độc lập mới nên hiện **chưa thể xác nhận đạt bonus**. Nhãn do AI đối chiếu, học viên vẫn cần xác nhận độc lập.

1. Cài phụ thuộc từ `requirements.txt`. API key chỉ đặt cục bộ trong `.env`; không đưa key vào Git hoặc trace.
2. Để dựng lại PDF trích, đặt bản PDF OpenStax gốc tại `.local/advanced_source_full.pdf`, kiểm tra SHA-256 gốc theo manifest, rồi chạy `python -X utf8 advanced/prepare.py`. Không cần đưa PDF đầy đủ vào gói nộp; PDF trích có giữ trang bản quyền/ghi công riêng.
3. So sánh cấu hình text-only và multimodal đã lưu tại `runs/dev-text/` và `runs/dev-vision/`. Mỗi cấu hình chạy đủ 18 câu/36 model call; text-only mất trung bình 3.282 giây/câu, ước tính $0.078257; vision mất 4.450 giây/câu, ước tính $0.159245. Chọn vision vì câu hỏi biểu đồ/sơ đồ cần đọc pixel, không chỉ đoạn text/caption; chấp nhận chi phí và thời gian cao hơn. Đây là quan sát dev, không phải điểm test.
4. Trước lần test đầu, chạy `python -X utf8 advanced/freeze.py`. Script kiểm tra số lượng/phân bổ câu, tách input khỏi gold, hai trang cho mọi câu multi-hop, manifest và hash; không ghi đè khóa đã có.
5. Chạy đúng một cấu hình đã khóa bằng `python -X utf8 advanced/workflow.py test`. Trace từng câu nằm tại `runs/test-vision/` và ghi truy vấn, xếp hạng trang, context, ảnh, tool call, câu trả lời, citation, thời gian, token, chi phí ước tính và lỗi.
6. Đối chiếu từng trace với PDF gốc, điền một nhãn pass/fail cùng lý do và kiểm tra nguồn cho từng ID vào `benchmark/test.review.json`, rồi chạy `python -X utf8 advanced/evaluate.py`. Lỗi/mất trace tính là không đạt; kết quả không được làm tròn để qua ngưỡng.

`benchmark/dev.json` có 15 câu trả lời được + 3 câu thiếu bằng chứng. `benchmark/test.json` có 30 câu: 24 trả lời được và 6 thiếu bằng chứng; các nhóm test có 6 bảng, 5 sơ đồ, 5 biểu đồ, 4 multi-hop và 4 text. `*.inputs.json` chỉ chứa ID, câu hỏi, nhóm; gold và evidence không được truyền vào pipeline.

Chạy multimodal cần API key, Internet và có thể phát sinh phí. Chi phí trong trace là ước tính theo usage/model, không thay thế hóa đơn. Chấm nguồn bằng AI hỗ trợ không thay thế việc học viên tự đọc và xác nhận nhãn trước khi nộp.
