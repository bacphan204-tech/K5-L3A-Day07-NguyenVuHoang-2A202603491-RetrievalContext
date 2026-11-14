# Báo cáo cá nhân Day 7 — Agentic RAG

**Họ và tên:** Nguyễn Vũ Hoàng  
**MSSV:** 2A202603491  
**Lớp:** L3A

## 1. Mục tiêu và dữ liệu sử dụng

Ở Day 7, em tiếp tục dùng dữ liệu sách kinh tế đã chuẩn bị trong Day 6. Mục tiêu là xây agent có thể tìm bằng chứng trong sách, trả lời tiếng Việt kèm nguồn và từ chối khi tài liệu không có đủ thông tin. Em thực hiện phần cơ bản của bài, chưa làm thử thách nâng cao với tài liệu từ 100 trang.

Tài liệu em sử dụng là *Principles of Economics 3e* của OpenStax, Rice University, phần chương 3 và 4 về cung–cầu, thị trường lao động và tài chính. File PDF rút gọn có 53 trang, gồm một trang bản quyền và 52 trang nội dung. Trang bản quyền không được đưa vào index. Nguồn và giấy phép CC BY-NC-SA 4.0 được giữ trong `data/day6/source_manifest.json` và PDF. Access for free at openstax.org.

Em chọn lại cấu hình B của Day 6, gồm 183 chunk. Cách chia ưu tiên ranh giới câu, tối đa 1.000 ký tự, không overlap và không ghép nội dung qua trang. Mỗi chunk giữ ID, nguồn, chương, trang PDF, trang in, trang PDF gốc và offset ký tự để tìm lại đoạn sách. Trường `page` là số trang trong PDF rút gọn, tính từ 1, khác với số in trên sách.

| Thành phần | Cấu hình sử dụng |
|---|---|
| Ngôn ngữ | Sách tiếng Anh, câu hỏi tiếng Việt |
| Embedding | `intfloat/multilingual-e5-small` |
| Revision | `614241f622f53c4eeff9890bdc4f31cfecc418b3` |
| Vector | 384 chiều, chuẩn hóa L2, chạy local CPU |
| Prefix | `query: ` cho câu hỏi, `passage: ` cho đoạn sách |
| Vector store | Chroma 1.5.9, collection `economics_b`, cosine/HNSW |
| Model agent | `gpt-5.4-mini-2026-03-17`, OpenAI Responses API |

Day 7 dùng bản sao database Day 6 để giữ nguyên dữ liệu đã làm. Phần chuẩn bị đã kiểm tra ID, nội dung, nguồn, trang, offset và hash PDF. Kiểm tra trích xuất lại PDF ghi nhận 52/52 trang nội dung có chữ và khớp phần đầu text đã chuẩn hóa. Tuy vậy, kiểm tra text không bảo đảm bảng, hình và bố cục được giữ đầy đủ; em chưa làm OCR hoặc xử lý hình bằng vision model.

## 2. Benchmark và nguyên tắc đánh giá

Em dùng bộ benchmark tối thiểu 24 câu, chia như sau:

| Loại câu | Dev | Test | Tổng |
|---|---:|---:|---:|
| Có đáp án trong tài liệu | 15 | 5 | 20 |
| Không đủ bằng chứng | 2 | 2 | 4 |
| **Tổng** | **17** | **7** | **24** |

Mười lăm câu dev có đáp án được dùng lại từ Day 6. Năm câu test có đáp án được soạn mới, không dùng lại năm câu test Day 6 đã xuất hiện trong phân tích và demo. Mỗi câu có ID, câu hỏi, đáp án, nguồn, trang và đoạn evidence. Nếu có nhiều evidence thay thế hợp lệ thì chỉ cần một phương án đủ ý. Bộ này chưa có câu bắt buộc ghép nhiều evidence theo schema multi-hop.

Các câu thiếu bằng chứng vẫn gần chủ đề sách nhưng hỏi dữ liệu cụ thể ngoài phạm vi tài liệu, chẳng hạn lương tối thiểu vùng I Việt Nam năm 2026. Mỗi câu có lý do, từ khóa kiểm tra trên cả 52 trang và các trang liên quan cần đọc lại. Em không xem việc top-k tìm rỗng là bằng chứng rằng cả tài liệu không có thông tin.

Các file `dev.inputs.json` và `test.inputs.json` chỉ chứa câu hỏi, ID, split và filter khi có. Đáp án, gold và nhãn có/thiếu bằng chứng nằm trong file riêng dành cho evaluator, không đưa vào model hoặc tool retrieval. Filter chương chỉ dùng khi người hỏi đã chỉ rõ chương, không lấy từ gold.

Em dùng dev để thử và chọn cấu hình, sau đó khóa trước khi chạy test. Test do AI hỗ trợ soạn và kiểm tra nguồn nên không phải bộ đánh giá mù độc lập bên ngoài. Các câu dev/test cũng cùng hai chương sách; kết quả không đại diện cho mọi câu hỏi kinh tế.

### Cách tính điểm

- **Hit@1, Evidence Hit@3:** số câu tìm được evidence hợp lệ trong top-1/top-3 chia số câu có đáp án. Cách chấm strict yêu cầu đúng nguồn, trang và chứa trọn một gold quote trong một chunk. Câu thiếu bằng chứng không nằm trong mẫu số này.
- **Context Evidence Rate:** số câu có đủ evidence trong context cuối gửi model chia số câu có đáp án. Em báo riêng kết quả khớp quote strict và kết quả đọc đối chiếu nguồn.
- **Context 0/1/2:** không có evidence; có nhưng thiếu điều kiện hoặc nguồn; đủ evidence và nguồn.
- **Grounded answer 0/1/2:** sai hoặc thiếu evidence; đúng một phần; đúng và đủ. Từ chối câu có đáp án được chấm 0.
- **Citation hợp lệ:** phải có trong context và hỗ trợ nội dung được trả lời. Đúng ID chưa đủ để tính đúng nghĩa.
- **Abstention:** từ chối câu thiếu evidence mà không thêm con số hoặc khẳng định suy đoán. Em cũng báo số câu có đáp án bị từ chối nhầm.

Phần lập trình, soạn câu hỏi và đánh giá có AI hỗ trợ. Nhãn trong `reviews.json` và `artifacts/*_review_decisions.json` do Codex AI đọc câu trả lời, context và nguồn rồi ghi điểm, lý do. Cùng AI cũng tham gia viết hệ thống nên có thể thiên lệch. Em chưa ghi nhận việc tự chấm độc lập toàn bộ nhãn; trường `student_confirmed` vẫn là `false`. Các bảng dưới cần được hiểu theo giới hạn này.

## 3. So sánh ba phương pháp retrieval

Em triển khai dense, BM25 và hybrid trên cùng 183 chunk B, cùng câu hỏi dev và cùng filter. Mỗi nhánh lấy tối đa 20 candidate, nhưng vẫn chấm ở cutoff 1 và 3 để so sánh. Thay top-k đơn thuần không được tính là một phương pháp mới.

| Phương pháp | Cách thực hiện |
|---|---|
| Dense | Tạo query embedding bằng E5 tương thích Day 6, tìm trong Chroma |
| BM25 | Khớp từ khóa, `k1=1,5`, `b=0,75`; chuẩn hóa Unicode NFC và chữ thường, tách token bằng `\w+` |
| Hybrid | Hợp nhất ranking dense/BM25 bằng RRF, `k=60`, trọng số bằng nhau |

Hybrid cộng đóng góp `1/(60 + rank)` của mỗi nhánh, không cộng trực tiếp raw score cosine với BM25. Kết quả giữ ID, text, score/rank, nguồn, trang và metadata.

| Phương pháp trên dev | Hit@1 | Strict Evidence Hit@3 | Median thời gian/query | Lỗi hệ thống |
|---|---:|---:|---:|---:|
| Dense | 2/15 (13,3%) | 6/15 (40,0%) | 48,32 ms | 0 |
| BM25 | 1/15 (6,7%) | 1/15 (6,7%) | 0,58 ms | 0 |
| Hybrid | 3/15 (20,0%) | 6/15 (40,0%) | 48,90 ms | 0 |

BM25 có kết quả thấp vì câu hỏi tiếng Việt còn nguồn tiếng Anh. Một số câu chỉ khớp số chương hoặc thuật ngữ Latin nên chưa tìm đúng nội dung. Em có thử tay từ khóa tiếng Anh nhưng giữ kết quả đó riêng, không trộn vào bảng query gốc. Hybrid tăng Hit@1 nhưng chưa tăng Hit@3 so với dense trong lượt này.

Trace và timing từng câu nằm ở `results/part05/dev-20261114T090138Z-f9b815/`. Retrieval chạy local nên phí API bằng 0 USD; em chưa đo điện và chi phí phần cứng.

## 4. Hai thí nghiệm cải thiện và phân tích lỗi

Sau khi đọc lỗi dev, em thử hai cấu hình đã ghi trong `artifacts/dev_improvement_plan.json` trước khi chạy:

1. **Dọn phần phạm vi trong query:** bỏ tiền tố “Theo chương 3/4” nếu cùng chương đã được truyền bằng filter. Giả thuyết là thông tin phạm vi lặp lại có thể làm nhiễu embedding. Nếu không có filter tương ứng thì giữ query gốc.
2. **Dọn query và sentence rerank:** dùng top-20 của cấu hình trên, tính `0,5 × dense cosine + 0,5 × cosine lớn nhất của một câu trong chunk`. Giả thuyết là embedding cả chunk dài có thể làm mờ câu chứa định nghĩa cần tìm.

Rerank vẫn dùng E5 cùng revision, prefix và chuẩn hóa L2. Chunk, ID và index Chroma không đổi; hệ thống tạo thêm vector câu, giữ offset để truy nguồn. Câu có độ tương đồng cao nhất chưa tự động được xem là evidence đúng.

| Cấu hình trên dev | Hit@1 | Strict Evidence Hit@3 | Median thời gian/query |
|---|---:|---:|---:|
| Dense ban đầu | 2/15 (13,3%) | 6/15 (40,0%) | 32,86 ms |
| Dọn query | 3/15 (20,0%) | 7/15 (46,7%) | 26,96 ms |
| Dọn query + sentence rerank | 7/15 (46,7%) | 9/15 (60,0%) | 56,98 ms |

Lần đầu cần mã hóa 1.182 câu, mất khoảng 13,2 giây ở lượt kiểm tra ban đầu, chưa gồm khởi tạo model. Các lượt sau dùng cache nên phải báo chi phí setup riêng, không xem việc dùng cache là không có chi phí tạo index câu. Bảng timing chỉ là một lượt đo trên máy, có tái sử dụng kết quả khi query không đổi, chưa đủ để kết luận tốc độ trong mọi điều kiện.

Hai lỗi em dùng để đặt giả thuyết:

- **d7-dev-q03 — cầu và lượng cầu:** các đoạn đầu tìm được nói về dịch chuyển đường cong hoặc ví dụ giá/lượng, nhưng thiếu định nghĩa cả đường cong so với một điểm. BM25 chỉ khớp token `3` từ số chương. Hai cách cải thiện vẫn chưa giải quyết hoàn toàn câu này.
- **d7-dev-q12 — giá trần:** dense có thể tìm đúng trang 26 nhưng lấy đoạn cân bằng nhà cho thuê thay vì định nghĩa. Sau sentence rerank, evidence định nghĩa vào top-3. Rerank cũng cải thiện Hit@3 ở q11 và q15 so với baseline.

Điều em rút ra là đúng trang hoặc đúng chủ đề chưa đủ. Em giữ kết quả trước/sau và cả ca không cải thiện trong `results/part06/dev-20261114T091322Z-474661/paired_changes.json`. Lượt tạo sentence bank đầu tiên được giữ riêng để kiểm tra chi phí setup.

## 5. Agent, context và kết quả đánh giá

Agent gọi OpenAI Responses API với model snapshot `gpt-5.4-mini-2026-03-17`. Hai tool là `search_book` và `finish_answer`; request đặt `store=false`. Model chọn query, có thể viết lại sang tiếng Anh, và quyết định tìm tiếp hay trả lời. Vì query do agent tạo có thể khác giữa hai pipeline, kết quả agent được báo riêng với benchmark query gốc ở trên.

Lượt đầu phải gọi retrieval. Giới hạn mỗi câu là 3 search và 4 lượt model. Mỗi search lấy 20 candidate, trả tối đa 5 chunk. Context budget là 5.000 ký tự, tính cả header nguồn. Hệ thống loại trùng ID, giữ nguyên chunk, bỏ chunk không vừa budget và ưu tiên ranking mới. Mỗi lượt chỉ gửi context hiện tại, không cộng dồn context cũ vượt budget. Nội dung tài liệu được xem là dữ liệu, không phải chỉ dẫn cho agent.

Trace giữ tool call, query, filter, candidate, context thực gửi model, câu trả lời, citation, lỗi, thời gian và token. Lỗi API được ghi thật; hệ thống không thay bằng kết quả mock. Lỗi citation hoặc định dạng từng câu vẫn được lưu để phân tích.

| Split / cấu hình | Số câu mức 0/1/2 | Grounded trung bình /2 | Context đủ evidence | Citation đúng nghĩa | Abstention đúng | Từ chối nhầm |
|---|---|---:|---:|---:|---:|---:|
| Dev / dense | 3/2/10 | 1,47 | 10/15 (66,7%) | 16/19 (84,2%) | 2/2 | 1/15 |
| Dev / rerank | 1/2/12 | 1,73 | 12/15 (80,0%) | 17/20 (85,0%) | 2/2 | 0/15 |
| Test / dense | 1/1/3 | 1,40 | 3/5 (60,0%) | 4/6 (66,7%) | 2/2 | 0/5 |
| Test / rerank | 0/0/5 | 2,00 | 5/5 (100,0%) | 7/7 (100,0%) | 2/2 | 0/5 |

Context mức 0/1/2 của dev dense là 2/3/10, dev rerank là 1/2/12; test dense là 1/1/3 và test rerank là 0/0/5. Nếu chỉ khớp gold quote strict, Context Evidence Rate dev là 8/15 và 9/15; test là 3/5 và 5/5. Điểm đối chiếu nghĩa dev cao hơn do có đoạn thay thế đủ ý nhưng khác gold. Em giữ cả hai cách tính, không sửa gold sau khi xem kết quả.

Tool use dev là 17/17 cho mỗi cấu hình, test là 7/7. Dev dense tìm một lần ở cả 17 câu; rerank có 16 câu tìm một lần và một câu tìm hai lần. Test mỗi câu tìm một lần. Tỷ lệ câu answered có citation lần lượt là 14/14, 15/15 trên dev và 5/5 cho mỗi cấu hình trên test. Chỉ số này khác tỷ lệ citation thực sự hỗ trợ nội dung trong bảng.

Lượt dev gốc có hai lỗi định dạng: dense/q08 có citation trong danh sách nhưng thiếu inline citation; rerank/u01 chọn abstain nhưng answer rỗng. Validator v1.2 xử lý hai trường hợp này, giữ raw decision và bản lỗi gốc. Bản revalidated chỉ kiểm tra lại offline, không gọi model mới. Việc thêm đúng ID model đã chọn vào văn bản chỉ sửa định dạng, không làm một nguồn sai trở thành đúng.

Các ca em cần lưu ý khi trình bày:

- **Câu có bằng chứng:** test q01 tính thặng dư tiêu dùng `90 − 80 = 10 USD`, có định nghĩa và số liệu tại trang 29.
- **Câu thiếu bằng chứng:** test hỏi giá xăng tại Hà Nội vào ngày cụ thể; agent từ chối, không dùng ví dụ USD/gallon trong sách để đoán.
- **Câu sai:** dev q08 trả lời đúng kiến thức về hàng hóa thứ cấp nhưng cite đoạn bưu chính, nên grounded answer chấm 0. Test dense/q02 nhầm thay đổi cầu với lượng cầu, còn q04 trả đúng kiến thức nhưng context không có evidence về niềm tin trả nợ.

### Chọn cấu hình trước test

Em chọn rerank vì grounded answer trung bình trên dev cao hơn. Tiêu chí so sánh tiếp theo là citation đúng nghĩa, context đủ và thời gian. Quy tắc chi tiết được ghi lúc lựa chọn sau các thử nghiệm dev, trước khi chạy test; đây không phải thí nghiệm dev đăng ký trước.

Cấu hình được khóa lúc `2026-11-14T09:50:35.989382+00:00` (UTC), với hash code, model/prompt/validator, corpus và benchmark trong `benchmark/frozen.json`. Sau đó baseline và cấu hình chọn chạy trên cùng 7 câu test. Em không đổi pipeline/gold sau khi xem test.

| Retrieval trên test | Hit@1 | Evidence Hit@3 |
|---|---:|---:|
| Dense, query gốc | 2/5 (40,0%) | 3/5 (60,0%) |
| Rerank, cleanup được ghi riêng | 4/5 (80,0%) | 4/5 (80,0%) |

Kết quả agent có thể cao hơn một lượt retrieval vì model được viết lại query và tìm thêm. Trên lượt test đã lưu, rerank có 5/5 câu có đáp án đạt mức 2 và từ chối đúng 2/2 câu thiếu evidence, không lỗi hệ thống. Tuy nhiên, tập chỉ có 7 câu nên em không xem đây là độ chính xác chung của hệ thống.

## 6. Chi phí, kiểm tra chạy lại và giới hạn

| Lượt / cấu hình | Lượt gọi model | Input token | Output token | API USD ước tính | Tổng thời gian agent |
|---|---:|---:|---:|---:|---:|
| Dev / dense | 34 | 32.855 | 2.193 | 0,034510 | 51,79 giây |
| Dev / rerank | 35 | 34.835 | 2.343 | 0,036670 | 56,47 giây |
| Test / dense | 14 | 13.896 | 1.090 | 0,015327 | 28,22 giây |
| Test / rerank | 14 | 13.968 | 1.065 | 0,015268 | 21,92 giây |

Chi phí hai batch chính khoảng 0,07118 USD cho dev và 0,03060 USD cho test, chưa gồm các lượt demo/probe. Đây là ước tính theo token và đơn giá ghi trong trace, không phải hóa đơn. Bản revalidated không phát sinh chi phí model mới. Request không trả usage có thể có chi phí chưa biết. Phần local chưa đo điện và phần cứng.

Tổng thời gian agent không gồm toàn bộ bước khởi tạo và tạo sentence bank. Timing retrieval test đã log chỉ tính phần dense, nên em không dùng cột đó để kết luận toàn bộ rerank nhanh hơn. Em chưa đo nhiều lượt độc lập để đánh giá độ biến động.

Trong lần hỏi thử sau benchmark, câu “Ai cung ứng lao động?” được gắn `STATUS: answered` nhưng agent lại giải thích tác động của công nghệ lên **cầu** lao động và chưa trả lời ai cung ứng lao động. Trace nằm ở `results/part07/20261114T100017Z-02e9bc/trace.json`. Ca này không nằm trong điểm test đã báo, nhưng cho thấy model có thể trả lời lệch câu hỏi dù citation ID hợp lệ. Em giữ nguyên pipeline đã khóa và ghi nhận đây là một giới hạn, không chỉnh theo ca mới rồi giữ nguyên kết luận test cũ.

Các giới hạn khác là câu hỏi Việt/nguồn Anh, corpus chỉ hai chương, bộ câu hỏi và nhãn có AI hỗ trợ, chưa xử lý tốt bảng/hình bằng phương pháp đa phương thức và chưa có xác nhận nhãn độc lập của học viên. Prompt, giới hạn vòng lặp và kiểm tra ID không bảo đảm mọi câu trả lời đều grounded hoặc chống được mọi chỉ dẫn độc hại trong tài liệu.

## 7. Cách chạy và vị trí minh chứng

README ở gốc repo ghi cách tái tạo dữ liệu, model và Chroma từ Day 6. Môi trường đã dùng là Windows, Python 3.14.6; các lệnh wrapper dùng venv Day 6. Model/index/venv không nộp kèm nhưng có hướng dẫn tạo lại. API key chỉ nằm trong `.env`, không đưa vào Git hoặc gói nộp.

Kiểm tra nhanh không gọi API:

```powershell
python -X utf8 -m unittest discover -s tests -v
python -X utf8 scripts/check_submission.py
python -X utf8 scripts/final_evaluation.py verify-lock
```

Hỏi thử bằng model thật, có tính phí API:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\ask_agent.ps1 -Question "Ai cung ứng lao động?" -Chapter 4
```

| Nội dung | Vị trí |
|---|---|
| Corpus, PDF và metadata | `data/day6/` |
| Benchmark dev/test, inputs, gold và khóa | `benchmark/` |
| So sánh ba phương pháp dev | `results/part05/dev-20261114T090138Z-f9b815/` |
| Hai cải thiện và kết quả từng câu | `results/part06/dev-20261114T091322Z-474661/` |
| Chi phí tạo sentence bank lần đầu | `results/part06/dev-20261114T090501Z-63b1b8/` |
| Dev agent gốc, gồm hai lỗi định dạng | `results/part08/dev-20261114T093751Z-4df860/` |
| Dev agent đã revalidate và nhãn | `results/part08/revalidated-20261114T094428Z-6d4f23/` |
| Trace và nhãn từng câu test | `results/final/test/` |
| Quyết định chấm và lý do của AI | `artifacts/dev_review_decisions.json`, `artifacts/test_review_decisions.json` |
| Kiểm tra nguồn PDF và bộ nộp | `results/final/source_verification.json`, `results/final/validation.json` |

Em đã có code, cấu hình, benchmark, trace, nhãn và báo cáo cho phần cơ bản. Trước khi nộp, em cần đọc hiểu các ca lỗi, tự xác nhận phần nhãn đã kiểm tra và bảo đảm giảng viên có quyền xem repo. Phần nâng cao không thực hiện; điểm cuối cùng do giảng viên đánh giá.
