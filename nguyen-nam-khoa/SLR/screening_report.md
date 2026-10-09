# Kết quả sàng lọc paper của Nguyễn Nam Khoa

Ngày tìm/đọc và ghi nhận: **09/10/2026**, múi giờ Asia/Saigon. Áp dụng query và IC/EC trong [protocol chung](../../team-synthesis/review_protocol.md) và [tiêu chí chung](../../team-synthesis/ie_criteria.md). Không sửa protocol của nhóm.

## Kết quả và phạm vi

Đã xử lý **20 mục trong ảnh**, bổ sung **2 paper về ChatTester/ChatUniTest**, tổng **22 records**. Sau bỏ một mục LM2Alloy bị lặp còn **21 paper độc lập**. Kết quả: **11 giữ**, **9 mục loại (1 trùng + 8 ngoài phạm vi)**, **2 chờ toàn văn**. Bảng evidence chung đã được điền 11 rows với mã `KHOA-*`; các mức CORE / METHOD SUPPORT / SUPPORTING / LOW_CONFIDENCE được ghi rõ, không xem cả 11 paper là bằng chứng trực tiếp ngang nhau.

**Giới hạn tìm kiếm:** Semantic Scholar (nguồn chính) và Google Scholar (bổ sung) đã được thử bằng query chung nhưng không trả danh sách kết quả truy cập được; các lần tải công khai trả HTTP 429. Vì vậy raw_hits của hai lượt này để trống, screened/candidate/included là 0 cho riêng các lượt bị chặn. Đây là kết quả sàng lọc danh sách gợi ý và tìm bổ sung có mục tiêu, **chưa phải một SLR đầy đủ từ hai cơ sở dữ liệu**. Không suy diễn '0 kết quả' từ lỗi truy cập.

```text
("unit test generation" OR "JUnit test suite" OR HumanEval) AND (ChatGPT OR Gemini OR "compiler-feedback repair" OR "structured prompting") AND (compilability OR executability OR "build success rate" OR "test execution rate")
```

Query trên giữ nguyên chuỗi của nhóm; bản gửi khi truy cập nằm trong search_log.csv và retrieval_log.json.

## Luồng sàng lọc

| Bước | Số mục | Diễn giải |
|---|---:|---|
| Seed từ ảnh | 20 | Số mục được cung cấp, không phải số hits Scholar |
| Bổ sung qua citation/title | 2 | ChatTester và ChatUniTest; nguồn arXiv được đối chiếu |
| Loại trùng | 1 | KHOA-014 trùng KHOA-013 |
| Paper độc lập còn lại | 21 | 19 seed + 2 bổ sung |
| Loại title/abstract ngoài phạm vi | 8 | EC1: 1; EC5: 7 |
| Giữ để đánh giá toàn văn | 13 | 11 có toàn văn + 2 chưa lấy được |
| Đã đọc và giữ sau toàn văn | 11 | Đã điền evidence; có ghi hạn chế chất lượng |
| Chờ toàn văn | 2 | Không đưa vào evidence cuối cùng |
| Loại sau đọc toàn văn | 0 | Đợt này không có; không cộng các loại TA vào số này |

`screened` ở seed log là 20 records đã được xử lý, gồm dedup; `candidate` là số retained để xét toàn văn, không phải toàn bộ file candidate_papers.csv. Các lượt title verification xác minh lại cùng paper, không cộng thêm vào luồng trên. Nguồn seed và tìm bổ sung được tách khỏi Scholar trong mọi bảng.

## Năm paper nên đọc trước

1. **KHOA-005 — Multi-LLM Chaining (2025):** gần nhất về HumanEval Java, GPT-4o và Gemini. Tables 2/3 có compile/runtime errors; Table 7 ghi Gemini 2.0 Flash và thời điểm model calls. Nhưng mẫu số là **từng test case sinh ra**, không phải suite của 30 bài. Không lấy 1 − compile-error-rate − runtime-error-rate làm tỷ lệ chung nếu chưa biết giao nhau/cách đếm.
2. **KHOA-021 — ChatTester (v3/2024):** định nghĩa compilation/pass và phân loại lỗi compiler/runtime rõ; Table 2 ghi compile 42.1%, pass 24.8% trên 1,000 tests ChatGPT. Sửa nhiều vòng; phần đánh giá bằng người là readability/usability, không phải human baseline compile/pass trên cùng bài.
3. **KHOA-006 — YATE (2025):** rất hữu ích cho tác động repair. Tables 2/3: class-level configuration có YATE compile 4,681/4,948 và pass 4,462/4,948. Không áp dụng kết quả của nhiều vòng repair + augmentation cho một vòng sửa của nhóm.
4. **KHOA-002 — TestART (v6):** đưa rule repairs, iterative repair và coverage feedback vào pipeline, reported passing 78.55% trên benchmark chính. Đơn vị focal method và không có Gemini/HumanEval; chỉ dùng để xây nền về repair/failure.
5. **KHOA-003 — Meta (2024):** giúp tách build, reliable pass, coverage. Ưu tiên cách diễn đạt Section 3.1: 75%/57%/25% **test classes có ít nhất một new test** đạt điều kiện. Abstract viết test cases, nên phải ghi chú sự khác biệt khi trích.

ChatUniTest (KHOA-022) dùng thêm cho context/validation/repair architecture. TCS, Oracle Audit, LM2Alloy và Business Requirements (KHOA-007/008/013/015) chỉ hỗ trợ oracle correctness/đánh giá. LLM-Test (KHOA-016) có số compile rate nhưng **độ tin cậy báo cáo thấp**: thiếu mẫu số, model snapshot/project versions và baseline được gọi cả GPT-4 lẫn Codex; giữ để mô tả có điều kiện, không tổng hợp số liệu định lượng cùng paper core.

## Quyết định từng mục

| ID | Paper / nguồn | Quyết định | Lý do chính |
|---|---|---|---|
| KHOA-001 | [Requirements-Based Test Generation: A Comprehensive Survey](https://arxiv.org/abs/2505.02015) | Loại | EC5: Survey rộng về sinh test từ requirements; không có bằng chứng thực nghiệm trực tiếp cho compile/run của JUnit do LLM sinh trong RQ này. |
| KHOA-002 | [TestART: Improving LLM-based Unit Testing via Co-evolution of Automated Generation and Repair Iteration](https://arxiv.org/html/2408.03095v6) | Giữ | IC1-IC5: Sinh unit test Java, repair dựa trên lỗi và báo cáo pass/compile; đọc được toàn văn. |
| KHOA-003 | [Automated Unit Test Improvement using Large Language Models at Meta](https://arxiv.org/html/2402.09171v1) | Giữ | IC1-IC5: Cải thiện unit tests bằng LLM trong sản phẩm thực tế; phân biệt build, pass và coverage; toàn văn có method/evaluation. |
| KHOA-004 | [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374) | Loại | EC1: Đối tượng thực nghiệm chính là chương trình do model sinh, không phải unit tests do model sinh. |
| KHOA-005 | [AI-Powered Unit Test Generation via Multi-LLM Chaining: A Case Study With GPT-4o, Gemini, and Claude-3.5](https://doi.org/10.1109/ACCESS.2025.3637221) | Giữ | IC1-IC5: JUnit/Java trên HumanEval, GPT-4o và Gemini; có compile/runtime metrics và toàn văn. |
| KHOA-006 | [YATE: The Role of Test Repair in LLM-Based Unit Test Generation](https://arxiv.org/html/2507.18316v1) | Giữ | IC1-IC5: Sinh unit test Java và ablation repair, có compilation/passing rates cùng mẫu số rõ; toàn văn truy cập được. |
| KHOA-007 | [Two-Stage Reinforcement Learning for Sound and Adversarial Test Generation in Code LLMs](https://arxiv.org/html/2609.03955v1) | Giữ | IC1-IC5: Sinh test bằng LLM và kiểm tra soundness/counterexample; đủ method/data, toàn văn preprint. |
| KHOA-008 | [Auditing and Decomposing Feedback-Driven Evolution in LLM Test Generation under the Oracle Problem](https://arxiv.org/html/2608.19626v1) | Giữ | IC1-IC5: LLM test generation, audit hiệu lực oracle/feedback, full-text method và evaluation truy cập được. |
| KHOA-009 | [Enhancing Mutation Testing Efficiency: A Comparative Study of Machine Learning Models for Equivalent Mutant Identification](https://doi.org/10.1002/stvr.70004) | Loại | EC5: Bằng chứng chính về phân loại equivalent mutants bằng ML, không về compilability/executability của tests do LLM sinh. |
| KHOA-010 | [A Multi-Stage Approach for LLM-Based Automated Repair of Test Cases](https://doi.org/10.1109/ICNLP69856.2026.11527996) | Chờ toàn văn | Chưa xác nhận IC4: hướng repair có thể phù hợp, nhưng publisher trả HTTP 202 với nội dung rỗng; chưa đủ toàn văn để quyết định. |
| KHOA-011 | [How Far Are We from Detecting Flaky Tests? On the Limits of Code-Based Detection](https://arxiv.org/abs/2607.09345) | Loại | EC5: Nghiên cứu phát hiện flaky tests từ code; không đánh giá lỗi compile/run của unit tests do LLM sinh. |
| KHOA-012 | [A Dataset of Reproducible Flaky-Test Failures](https://arxiv.org/abs/2605.21677) | Loại | EC5: Dataset tái hiện flaky failures của tests hiện có; không có thực nghiệm sinh JUnit bằng LLM hữu ích trực tiếp cho RQ. |
| KHOA-013 | [LM2Alloy: Investigating LLM-Generated Formal Specifications for Automated Test Derivation in Production Software](https://arxiv.org/html/2607.18555v1) | Giữ | IC1-IC5: LLM sinh formal specs để suy ra tests, đánh giá executable/correctness/coverage; toàn văn đủ method. |
| KHOA-014 | [LM2Alloy: Investigating LLM-Generated Formal Specifications for Automated Test Derivation in Production Software](https://arxiv.org/abs/2607.18555) | Loại | EC3: Mục trùng KHOA-013; cùng tác giả và arXiv 2607.18555, không phải nghiên cứu độc lập. |
| KHOA-015 | [From Business Requirements to Test Assertions: Evaluating LLM-Generated Oracles on Real Bugs](https://arxiv.org/html/2607.10277v1) | Giữ | IC1-IC5: Sinh test assertions/oracles Java bằng LLM trên bugs thật; có phương pháp, model, dữ liệu và toàn văn. |
| KHOA-016 | [Large Language Models for Automated Software Test Generation](https://doi.org/10.63090/IJITRS/3139.3209.0022) | Giữ | IC1-IC5: Java unit-test generation, mô tả GPT-4/data/evaluation và compile rate; toàn văn truy cập được. Giữ có cảnh báo chất lượng báo cáo. |
| KHOA-017 | [PYURIFY: Purifying Python Tests for Precise Fault Localization](https://doi.org/10.1145/3803437.3806433) | Loại | EC5: Công cụ tách/purify tests Python hiện có để fault localization; không cung cấp bằng chứng LLM-generated JUnit compile/run. |
| KHOA-018 | [FailMapper: Automated Generation of Unit Tests Guided by Failure Scenarios](https://doi.org/10.1109/ASE63991.2025.00197) | Chờ toàn văn | Chưa xác nhận IC4: abstract phù hợp test generation/failure scenarios nhưng chưa lấy được toàn văn nghiên cứu. |
| KHOA-019 | [LLM-Augmented Mutation Testing: Intelligent Generation and Triage of Mutants](https://doi.org/10.1109/ICAISET66439.2026.11541746) | Loại | EC5: Sinh/triage mutants, không đánh giá compilability/executability của unit tests do LLM sinh cho RQ. |
| KHOA-020 | [230,439 Test Failures Later: An Empirical Evaluation of Flaky Failure Classifiers](https://arxiv.org/abs/2401.15788) | Loại | EC5: Phân loại flaky/real failures từ tests hiện có, không phải sinh JUnit bằng ChatGPT/Gemini. |
| KHOA-021 | [No More Manual Tests? Evaluating and Improving ChatGPT for Unit Test Generation](https://arxiv.org/html/2305.04207v3) | Giữ | IC1-IC5: Java unit tests do ChatGPT sinh, đo compile/pass và phân tích lỗi; ChatTester repair, đủ full-text method. |
| KHOA-022 | [ChatUniTest: A Framework for LLM-Based Test Generation](https://arxiv.org/html/2305.04764v2) | Giữ | IC1-IC5: Framework sinh Java tests có validate/repair, đánh giá coverage, đủ model/dataset và full text. |

## Hai paper chờ toàn văn

- **KHOA-010 — Multi-Stage Repair:** metadata phụ gợi ý phù hợp, nhưng IEEE trả HTTP 202 với nội dung rỗng. Tác giả/pp.536-540 hiện dựa trên metadata phụ, cần đối chiếu bản chính. Chưa trích tỷ lệ compile/pass hay đánh dấu IC2/IC3/IC4 đã đạt. Cần PDF hợp lệ từ publisher hoặc author manuscript để xét tiếp.
- **KHOA-018 — FailMapper:** institutional abstract xác nhận hướng unit-test generation theo failure scenarios; repository có artifacts/technical documentation. Chưa lấy được toàn văn research paper để kiểm tra model, repair budget, mẫu số và metrics. Repo/abstract không thay cho toàn văn. Cần PDF publisher/author manuscript để xét tiếp.

Hai record giữ trạng thái `PENDING_FULL_TEXT`, **chưa phải full-text exclusion EC4**. Khi có toàn văn thì điền IC1-IC5; nếu chốt không lấy được toàn văn theo quy trình của nhóm mới ghi EC4, một lý do chính. Các mục đã loại ở title/abstract không bị trình bày như đã đọc toàn văn.

## Evidence dùng được cho RQ của nhóm

Trong **tập paper đã đọc ở đợt này**, chưa thấy nghiên cứu đáp ứng đồng thời: 30 HumanEval Java cố định; human test viết trước khi xem AI; ChatGPT/Gemini cùng structured prompt; đúng một compiler-feedback repair; paired binary outcome 'toàn bộ suite compile và chạy pass'; phân tích theo task category. Đây là nhận xét trong tập đã đọc, **không phải khẳng định toàn bộ literature chưa có** vì Scholar search chưa hoàn tất.

Evidence hiện hỗ trợ ba điểm: LLM-generated tests có compile/runtime failures; feedback/repair có thể cải thiện tính hợp lệ trong các pipeline khác; đánh giá cần tách compile, execution và oracle correctness. Các paper core dùng model/dataset/repair budget/đơn vị phân tích khác nhau nên **không gộp tỷ lệ thành một hiệu ứng chung**.

Với thí nghiệm 30 bài của nhóm, lưu riêng mỗi bài/nguồn: compile được hay không, toàn bộ tests pass hay không, kết quả trước và sau đúng một vòng repair, error text/type. Mẫu số cuối cùng vẫn là 30 bài mỗi nguồn và giữ cả các bài AI không compile. Human baseline là bài do người viết trước khi xem AI; coverage hoặc đánh giá readability trong papers không cung cấp baseline này.

Phân loại lỗi như missing symbol/type/access/assertion failure từ ChatTester là **failure taxonomy**, khác **task categories** của HumanEval. Không lấy taxonomy lỗi làm category của bài. Categories, prompt, model versions và giới hạn repair phải chốt trước khi so sánh kết quả; không điều chỉnh từ tỷ lệ trong paper.

## Hồ sơ đã lưu

- [Search log của Khoa](search_log.csv) và [search log chung](../../team-synthesis/search_log.csv): query, ngày, counts, blocked status và nguồn bổ sung.
- [Danh sách ứng viên/quyết định](candidate_papers.csv): 22 records, một lý do loại chính.
- [Audit title/full-text](fulltext_screening.csv): stage, IC1-IC5, file đã đọc, vị trí bằng chứng, đơn vị/mẫu số, repair budget và reporting limitations.
- [Evidence chung](../../team-synthesis/evidence_table.csv): 11 papers đã đọc toàn văn; provenance và giới hạn so sánh.
- [Title verification log](title_verification_log.csv): chuỗi title lookup được chuẩn hóa để tìm lại và record URLs; không phải bản lưu nguyên văn từng biến thể web query. Unknown raw hits để trống.
- [Nguồn toàn văn](sources/README.md), các snapshots HTML/PDF/text, retrieval log và ảnh kiểm tra Tables 2/3/7 của Chaining, Table 2/setup/limitations của LLM-Test.

Các public artifact links là thông tin paper công bố; đợt này không chạy code tái lập, không xác nhận package hoạt động. Không thu thập citation counts từ nguồn bị chặn.
