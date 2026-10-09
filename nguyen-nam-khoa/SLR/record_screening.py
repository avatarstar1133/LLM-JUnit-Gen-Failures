"""Record the 2026-10-09 screening batch; preserve other members' rows."""
from pathlib import Path
import csv
import json
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATE = '2026-10-09'
QUERY = '("unit test generation" OR "JUnit test suite" OR HumanEval) AND (ChatGPT OR Gemini OR "compiler-feedback repair" OR "structured prompting") AND (compilability OR executability OR "build success rate" OR "test execution rate")'
papers = []

def paper(number, title, authors, year, url, decision, reason, notes, **extra):
    papers.append(dict(paper_id=f'KHOA-{number:03}', title=title, authors=authors,
                       year=year, doi_or_url=url, decision=decision, reason=reason,
                       notes=notes, **extra))

paper(1, 'Requirements-Based Test Generation: A Comprehensive Survey',
      'Zhenzhen Yang; Rubing Huang; Chenhui Cui; Nan Niu; Dave Towey', 2025,
      'https://arxiv.org/abs/2505.02015', 'EXCLUDE',
      'EC5: Survey rộng về sinh test từ requirements; không có bằng chứng thực nghiệm trực tiếp cho compile/run của JUnit do LLM sinh trong RQ này.',
      'Title/abstract screening. Giữ làm tài liệu nền và nguồn snowball ngoài evidence chính. Năm 2025 là preprint; không trộn với journal version 2026.')

paper(2, 'TestART: Improving LLM-based Unit Testing via Co-evolution of Automated Generation and Repair Iteration',
      'Siqi Gu; Quanjun Zhang; Kecheng Li; Chunrong Fang; Fangyuan Tian; Liuchuan Zhu; Jianyi Zhou; Zhenyu Chen', 2024,
      'https://arxiv.org/html/2408.03095v6', 'INCLUDE',
      'IC1-IC5: Sinh unit test Java, repair dựa trên lỗi và báo cáo pass/compile; đọc được toàn văn.',
      'CORE. Preprint đầu tiên 2024; trích xuất từ v6 ngày 2025-03-31, không trộn số liệu giữa versions.',
      source='sources/testart_v6.html', location='Sections 3-5; Table 2; threats to validity',
      tool='TestART; ChatGPT-3.5; GPT-4 baseline',
      dataset='Defects4J: 8,192 focal methods / 5 Java projects; HITS: 885; industrial set: 668',
      setting='JUnit 4 / JDK 1.8; rule-based repairs + iterative LLM repair + coverage-guided prompting; repeated experiments',
      metric='Passing rate; compilation/runtime error rates; coverage. Đơn vị: focal method với generated tests.',
      result='Table 2: TestART passing 78.55%; ChatGPT-3.5 49.91%; GPT-4 59.75%; ChatUniTest 60.05%.',
      code='Reported public artifact: https://github.com/sikygu/TestART (chưa chạy tái lập)',
      limits='Nhiều vòng repair và tăng coverage; không HumanEval/Gemini/human paired baseline. Coverage trên tests đã qua kiểm tra, không thay thế tỷ lệ compile-and-run trên toàn bộ bài.',
      relevance='CORE: compiler-feedback repair, nguyên nhân lỗi và cách tách pass/compile; không phải bằng chứng cho đúng protocol một vòng sửa của nhóm.',
      unit='focal method', denominator='8,192 focal methods in main benchmark; Table 2 reported percentages',
      repair='Iterative, rule-based + LLM + coverage feedback; more than one round', quality='MEDIUM; research preprint; external validity limitations')

paper(3, 'Automated Unit Test Improvement using Large Language Models at Meta',
      'Nadia Alshahwan; Jubin Chheda; Anastasia Finogenova; Beliz Gokkaya; Mark Harman; Inna Harper; Alexandru Marginean; Shubho Sengupta; Eddy Wang', 2024,
      'https://arxiv.org/html/2402.09171v1', 'INCLUDE',
      'IC1-IC5: Cải thiện unit tests bằng LLM trong sản phẩm thực tế; phân biệt build, pass và coverage; toàn văn có method/evaluation.',
      'CORE. Trích Section 3.1 theo test classes, tránh lấy cách diễn đạt test cases trong abstract làm mẫu số.',
      source='sources/meta_v1.html', location='Sections 2-3; Section 3.1; limitations',
      tool='TestGen-LLM; two internal LLMs (LLM1 / LLM2)',
      dataset='Kotlin unit-test classes for Instagram Reels and Stories at Meta',
      setting='Improve existing human-written test classes; generate candidates; build/reliability/coverage filters',
      metric='Build success; reliable pass; coverage improvement. Section 3.1: test classes with at least one qualifying new test.',
      result='75% classes contain >=1 new test that builds; 57% contain >=1 that builds and passes reliably; 25% contain >=1 that also improves line coverage.',
      code='No public replication code verified; proprietary products and internal models',
      limits='Abstract/result wording differs in aggregation; Section 3.1 is class-level at-least-one. Kotlin; internal data/models; no fresh HumanEval JUnit generation or paired human success rate.',
      relevance='CORE: staged validation and separate build/pass outcomes; only methodological support for the group setting.',
      unit='test class with at least one qualifying new test', denominator='Evaluated test classes in Section 3.1; do not reinterpret as pooled generated test cases',
      repair='Candidate generation / filtering / improvement pipeline; not one fixed compiler-repair experiment', quality='MEDIUM; industrial study; restricted reproducibility')

paper(4, 'Evaluating Large Language Models Trained on Code',
      'Mark Chen et al.', 2021, 'https://arxiv.org/abs/2107.03374', 'EXCLUDE',
      'EC1: Đối tượng thực nghiệm chính là chương trình do model sinh, không phải unit tests do model sinh.',
      'Title/abstract screening. Giữ riêng làm nguồn HumanEval 164 Python problems; không điền như bằng chứng JUnit compile/run.')

paper(5, 'AI-Powered Unit Test Generation via Multi-LLM Chaining: A Case Study With GPT-4o, Gemini, and Claude-3.5',
      'Chandan Kumar; Usha Sri Ponaka; Pula V. Lakshmi Narasimha Naidu; Pyatlo Bhuvaneswari; Mukesh Prasad; Sunil Kumar Singh', 2025,
      'https://doi.org/10.1109/ACCESS.2025.3637221', 'INCLUDE',
      'IC1-IC5: JUnit/Java trên HumanEval, GPT-4o và Gemini; có compile/runtime metrics và toàn văn.',
      'CORE; gần dataset/models nhất. IEEE Access 13:204058-204071. Nguồn PDF publisher đã đọc và kiểm tra hình ảnh bảng.',
      source='sources/chaining_fulltext.pdf', location='Tables 2-3 and 7; Algorithms 2-3; validity discussion; appendix',
      tool='GPT-4o; Gemini 2.0 Flash; Claude 3.5 Sonnet; Gemini -> GPT-4o / Claude chaining',
      dataset='HumanEval Java conversion, described as 164 tasks; no frozen 30-task list matching the group',
      setting='Single-model and multi-model chains; structured prompts; invalid-output retry and coverage-driven iterations; August 2025 model calls',
      metric='Compilation errors / all generated test cases; runtime failures / all generated test cases; line/branch coverage; mutation score',
      result='Table 2: Gemini compilation errors 13/3,077 (0.42%); GPT-4o 18/2,454 (0.73%). Table 3: runtime failures Gemini 301/3,077 (9.78%); GPT-4o 375/2,454 (15.28%).',
      code='Reported artifact: https://github.com/ushasri3110/LLMChaining (chưa chạy tái lập)',
      limits='Counts are generated test cases, not 30 problem-level suites. Runtime denominators are total generated tests; overlap/conditional execution not established. No paired human baseline, one-repair control or task-category comparison. Cannot derive the group joint success rate by subtracting both error rates.',
      relevance='CORE / first priority: same HumanEval Java and GPT/Gemini family; motivates compile/runtime comparison but does not answer the exact paired RQ.',
      unit='generated test case', denominator='Gemini 3,077; GPT-4o 2,454; chain/model-dependent totals',
      repair='Invalid-output retries and coverage-based iterative chaining; not one compiler-feedback round', quality='MEDIUM; unit-of-analysis mismatch and manual/iterative handling need care')

paper(6, 'YATE: The Role of Test Repair in LLM-Based Unit Test Generation',
      'Michael Konstantinou; Renzo Degiovanni; Jie M. Zhang; Mark Harman; Mike Papadakis', 2025,
      'https://arxiv.org/html/2507.18316v1', 'INCLUDE',
      'IC1-IC5: Sinh unit test Java và ablation repair, có compilation/passing rates cùng mẫu số rõ; toàn văn truy cập được.',
      'CORE. Trích v1; class-level configuration khác method-level configuration.',
      source='sources/yate_v1.html', location='Approach/evaluation sections; Tables 2-3; ablations; threats',
      tool='YATE; GPT-4o-mini primary; robustness with GPT-4.1 / DeepSeek-V3 / Codestral',
      dataset='6 Java projects; 393 classes; 3,657 methods',
      setting='JUnit 5; JDK 8/11/17 by project; static repairs + LLM repair + test augmentation; LLM-Plain baseline',
      metric='Compilation and passing rates in class-level and method-level generation configurations; branch coverage/mutation',
      result='Class-level configuration: LLM-Plain compile 2,865/3,232=88.64%, pass 1,633/3,232=50.53%; YATE compile 4,681/4,948=94.60%, pass 4,462/4,948=90.18%.',
      code='Reported artifact: https://github.com/michaelkonstantinou/yate-java (chưa chạy tái lập)',
      limits='Different generated-test counts across approaches; not paired HumanEval problems. Multiple repair rounds (including oracle fixes) and augmentation; coverage evaluated after validation. No Gemini/human paired baseline.',
      relevance='CORE: shows repair effects and explicit denominators; extract repair design, do not import rates into the one-repair group experiment.',
      unit='generated tests within class-level or method-level generation configuration', denominator='Class-level configuration: 3,232 LLM-Plain; 4,948 YATE generated tests',
      repair='Rule/static + LLM repair; up to 3 oracle-fix iterations, iterative compilation repair and augmentation', quality='MEDIUM; preprint; repair-budget and population differences')

paper(7, 'Two-Stage Reinforcement Learning for Sound and Adversarial Test Generation in Code LLMs',
      'Jiacheng Xu; Wentao Zhang; Zhiyi Lyu; Fuxiang Zhang; Chaojie Wang; Yang Liu; Bo An', 2026,
      'https://arxiv.org/html/2609.03955v1', 'INCLUDE',
      'IC1-IC5: Sinh test bằng LLM và kiểm tra soundness/counterexample; đủ method/data, toàn văn preprint.',
      'SUPPORTING: ground-truth validation; không phải bằng chứng JUnit compile rate.',
      source='sources/tcs_v1.html', location='Method; experimental evaluation; Appendix A.2',
      tool='TCS; DeepSeek-R1-Distill-Qwen 1.5B / 7B',
      dataset='TACO: 6,318 curated training tasks / 1,000 validation tasks; LiveCodeBench evaluation',
      setting='Two-stage RL for a Python test generator; reference-checked soundness then adversarial counterexamples',
      metric='Test soundness/counterexamples; downstream solver pass@1 and best-of-N are program outcomes',
      result='Reports improvement in sound/adversarial test generation and downstream code selection. Solver pass@1 is not generated-test compilation/execution success.',
      code='Repository link reported in paper Appendix A.2; artifact execution not verified',
      limits='Python algorithmic tasks; trained small models; no Java/GPT/Gemini or compiler-feedback one-repair protocol. Do not relabel solver pass@1 as test pass rate.',
      relevance='SUPPORTING: reference validation and test-oracle correctness; contextual evidence only.',
      unit='generated input/output test and downstream code solution (distinct outcomes)', denominator='Task/test/solver-specific; no JUnit compile-and-run denominator',
      repair='RL training and test sampling, not fixed compiler-feedback repair', quality='MEDIUM; recent preprint; indirect RQ relevance')

paper(8, 'Auditing and Decomposing Feedback-Driven Evolution in LLM Test Generation under the Oracle Problem',
      'Yunhao Liang; Chengguang Gan; Ruixuan Ying; Hanjun Wei; Zhe Cui; Shiwen Ni', 2026,
      'https://arxiv.org/html/2608.19626v1', 'INCLUDE',
      'IC1-IC5: LLM test generation, audit hiệu lực oracle/feedback, full-text method và evaluation truy cập được.',
      'SUPPORTING: evaluation bias / oracle problem; không dùng làm tỷ lệ JUnit chạy thành công.',
      source='sources/oracle_audit_v1.html', location='Evaluation setup; audit experiments; limitations',
      tool='Qwen2.5-Coder-7B; Qwen3.5-9B without thinking',
      dataset='Algorithmic tasks: 142 development, 114 external and 138 held-out audit tasks',
      setting='Python/JSONL tests; cross-fitted oracle panel; placebo feedback; budget-matched resampling; three seeds',
      metric='Oracle-conditioned test gain; audit-panel gain; resampling vs mutation',
      result='Single-oracle evaluation inflates apparent gains by 9.46-14.85 percentage points; budget-matched resampling exceeds mutation by 6.01-18.83 points in the reported audits.',
      code='Reported anonymous artifact: https://anonymous.4open.science/r/llm-test-evolution-audit-8CF5/ (not executed)',
      limits='Python task/input-output evaluation; no JUnit compilation or target models. Audit metrics are not overall build/run rates; recent preprint.',
      relevance='SUPPORTING: avoid favorable oracle/selection bias; independent validation and matched feedback budgets.',
      unit='algorithmic task / generated test evaluated against oracle panel', denominator='Audit-specific task sets; no group 30-problem JUnit denominator',
      repair='Feedback-driven test mutation/resampling audit, not compiler repair', quality='MEDIUM; recent preprint; indirect RQ relevance')

paper(9, 'Enhancing Mutation Testing Efficiency: A Comparative Study of Machine Learning Models for Equivalent Mutant Identification',
      'Terrence Pugh; Carlos Mina Lopez; Samuel Peacock; Lin Deng; Josh Dehlinger; Suranjan Chakraborty', 2025,
      'https://doi.org/10.1002/stvr.70004', 'EXCLUDE',
      'EC5: Bằng chứng chính về phân loại equivalent mutants bằng ML, không về compilability/executability của tests do LLM sinh.',
      'Title/abstract screening. Wiley primary abstract; mutation triage khác test generation failure.')

paper(10, 'A Multi-Stage Approach for LLM-Based Automated Repair of Test Cases',
      'Xiaoyin Wang; Zhaorong Ji; Yao Wang; Mengfan Liu [secondary metadata; primary author list not verified]', 2026,
      'https://doi.org/10.1109/ICNLP69856.2026.11527996', 'PENDING_FULL_TEXT',
      'Chưa xác nhận IC4: hướng repair có thể phù hợp, nhưng publisher trả HTTP 202 với nội dung rỗng; chưa đủ toàn văn để quyết định.',
      'TA provisionally relevant from title/secondary abstract. IEEE ICNLP 2026 pp.536-540 metadata cần đối chiếu PDF. Không trích số kết quả thứ cấp vào evidence.',
      source='', location='Title / secondary metadata only; full text unavailable in this session')

paper(11, 'How Far Are We from Detecting Flaky Tests? On the Limits of Code-Based Detection',
      'Ömer Oktay Gültekin; Alexander Berndt; Jonathan Bell; Thomas Bach; Sebastian Baltes', 2026,
      'https://arxiv.org/abs/2607.09345', 'EXCLUDE',
      'EC5: Nghiên cứu phát hiện flaky tests từ code; không đánh giá lỗi compile/run của unit tests do LLM sinh.',
      'Title/abstract screening. Không đồng nhất flaky failure với lỗi test code do AI sinh.')

paper(12, 'A Dataset of Reproducible Flaky-Test Failures',
      'Suzzana Rafi; Mahbub-Ul-Hoque Sumon; Md Erfan; Maruf Morshed Khan; August Shi; Wing Lam', 2026,
      'https://arxiv.org/abs/2605.21677', 'EXCLUDE',
      'EC5: Dataset tái hiện flaky failures của tests hiện có; không có thực nghiệm sinh JUnit bằng LLM hữu ích trực tiếp cho RQ.',
      'Title/abstract screening. Có thể dùng riêng cho phần validity nếu cần.')

paper(13, 'LM2Alloy: Investigating LLM-Generated Formal Specifications for Automated Test Derivation in Production Software',
      'Tasmim Rashid; Muhammad Zubair Malik', 2026,
      'https://arxiv.org/html/2607.18555v1', 'INCLUDE',
      'IC1-IC5: LLM sinh formal specs để suy ra tests, đánh giá executable/correctness/coverage; toàn văn đủ method.',
      'SUPPORTING. Metadata title là LM2Alloy; heading trong full text dùng LLM2Alloy. Hai mục trong ảnh là cùng paper.',
      source='sources/llm2alloy_v1.html', location='Approach; case studies; results; limitations',
      tool='GPT-4o web interface; Alloy Analyzer; pytest',
      dataset='Two Python production libraries: Flipper and Cerberus',
      setting='Manually select code/docs context; LLM -> Alloy specification -> derived tests; three fresh sessions per prompt',
      metric='Specification validity; executable derived tests; branch coverage / detected behavioral errors',
      result='Reports valid specifications and executable derived tests without manual correction; finds behavior missed by direct LLM tests. No aggregate JUnit compile/pass numerator and denominator.',
      code='Subject repositories linked; separate replication package not verified',
      limits='Two Python case studies; web interface and selected context; no target Java models/one-repair experiment. Qualitative executability statement cannot yield a 30-task rate.',
      relevance='SUPPORTING: structured specifications and oracle correctness; indirect evidence for prompting/validation.',
      unit='specification / derived tests in two case studies', denominator='No aggregate compile-and-run denominator reported for the group outcome',
      repair='Formal derivation / validation, not one compiler-feedback round', quality='MEDIUM; small case studies; preprint; indirect RQ relevance')

paper(14, 'LM2Alloy: Investigating LLM-Generated Formal Specifications for Automated Test Derivation in Production Software',
      'Tasmim Rashid; Muhammad Zubair Malik', 2026,
      'https://arxiv.org/abs/2607.18555', 'EXCLUDE',
      'EC3: Mục trùng KHOA-013; cùng tác giả và arXiv 2607.18555, không phải nghiên cứu độc lập.',
      'Deduplication before TA/full text; giữ KHOA-013, không nhân đôi evidence.')

paper(15, 'From Business Requirements to Test Assertions: Evaluating LLM-Generated Oracles on Real Bugs',
      'Tiancheng Ma; Nasir U. Eisty', 2026,
      'https://arxiv.org/html/2607.10277v1', 'INCLUDE',
      'IC1-IC5: Sinh test assertions/oracles Java bằng LLM trên bugs thật; có phương pháp, model, dữ liệu và toàn văn.',
      'SUPPORTING: oracle correctness; đặc biệt ghi nhận một output không compile bị loại khỏi một phép tính trong paper.',
      source='sources/business_oracles_v1.html', location='Setup; evaluation tables including Table 3; validity',
      tool='DeepSeek-V3; Gemma3n; Llama3; Mistral-7B; Qwen3',
      dataset='10 Defects4J Lang bugs (1 and 3-11); Java test oracles',
      setting='Requirements/SUT/manual oracle comparison; five LLMs; pilot evaluation',
      metric='Accuracy / precision / recall / F1 of generated oracles; correlation with requirement completeness',
      result='Performance varies across bugs/models. Table 3 uses 9 observations for Mistral because one generated oracle does not compile; other models use 10. Correlation CIs include zero.',
      code='Reported dataset: https://figshare.com/s/50c240d183532de44c7a (not executed)',
      limits='Small pilot; no GPT/Gemini; assertion/oracle generation differs from full suite. Noncompiling output excluded from some metrics: group must retain such cases in its all-problem failure denominator.',
      relevance='SUPPORTING: assertion validity and denominator/selection bias; no direct compile-and-run success comparison.',
      unit='bug / generated oracle', denominator='10 bugs; Mistral has 9 after excluding one noncompiling result in Table 3',
      repair='Oracle generation, not fixed compiler-feedback repair', quality='MEDIUM; small preprint pilot; selection bias explicitly tracked')

paper(16, 'Large Language Models for Automated Software Test Generation',
      'Juby George', 2026, 'https://doi.org/10.63090/IJITRS/3139.3209.0022', 'INCLUDE',
      'IC1-IC5: Java unit-test generation, mô tả GPT-4/data/evaluation và compile rate; toàn văn truy cập được. Giữ có cảnh báo chất lượng báo cáo.',
      'LOW_REPORTING_CONFIDENCE; descriptive evidence only. IJITRS 2(2), pp.52-58. Baseline identity differs between setup/Table 2 (GPT-4) and result prose/Fig.2 (Codex).',
      source='sources/llm_test_fulltext.pdf', location='Sections IV-VI; Table 2; PDF pages 4-6 / printed pp.55-57',
      tool='LLM-Test; GPT-4 primary per methods; zero-shot baseline ambiguously also labeled Codex',
      dataset='Apache Commons CLI; Gson; JFreeChart; FastJSON',
      setting='Context/coverage/mutation feedback; up to 10 refinement rounds; five repetitions',
      metric='Compilation rate; branch coverage; mutation score; detected bugs',
      result='Table 2 reports compile 94.1% LLM-Test vs 87.6% few-shot GPT-4 and 82.3% zero-shot GPT-4; branch coverage 81.5% for LLM-Test. Exact compilation numerator/denominator not reported.',
      code='No replication code/raw-data link verified in full text',
      limits='LOW reporting confidence: unspecified model snapshot/project versions and compile denominator; baseline GPT-4/Codex inconsistency. Ten rounds differ from one repair. Do not quantitatively pool these values or use as sole support for RQ.',
      relevance='SUPPORTING / LOW_CONFIDENCE: compiler/feedback context only; not core quantitative evidence.',
      unit='Not clearly specified for compilation rate', denominator='Not reported; Table 2 percentages only',
      repair='Up to 10 coverage/mutation feedback refinement rounds', quality='LOW_REPORTING_CONFIDENCE; baseline identity and reproducibility concerns')

paper(17, 'PYURIFY: Purifying Python Tests for Precise Fault Localization',
      'Marius Smytzek; Andreas Zeller', 2026, 'https://doi.org/10.1145/3803437.3806433', 'EXCLUDE',
      'EC5: Công cụ tách/purify tests Python hiện có để fault localization; không cung cấp bằng chứng LLM-generated JUnit compile/run.',
      'Title/abstract screening; FSE 2026 tool-demonstration abstract.')

paper(18, 'FailMapper: Automated Generation of Unit Tests Guided by Failure Scenarios',
      'Ruiqi Dong; Zehang Deng; Xiaogang Zhu; Xiaoning Du; Huai Liu; Shaohua Wang; Sheng Wen; Yang Xiang', 2025,
      'https://doi.org/10.1109/ASE63991.2025.00197', 'PENDING_FULL_TEXT',
      'Chưa xác nhận IC4: abstract phù hợp test generation/failure scenarios nhưng chưa lấy được toàn văn nghiên cứu.',
      'TA retained. Primary abstract: https://research.monash.edu/en/publications/failmapper-automated-generation-of-unit-tests-guided-by-failure-s/ . Repo https://github.com/nuwaLab/FailMapper có artifacts/technical docs, không thay thế full text. ASE 2025 pp.2388-2400.',
      source='', location='Primary institutional abstract; artifact repository checked; no research full text retrieved')

paper(19, 'LLM-Augmented Mutation Testing: Intelligent Generation and Triage of Mutants',
      'Sanjay Bajaj; Venkata Seetarama Raju Dantuluri; Devendra Rajput; Anil Kolhe', 2026,
      'https://doi.org/10.1109/ICAISET66439.2026.11541746', 'EXCLUDE',
      'EC5: Sinh/triage mutants, không đánh giá compilability/executability của unit tests do LLM sinh cho RQ.',
      'Title/abstract screening. Mutation score/mutant triage không đồng nghĩa generated-test compile/run.')

paper(20, '230,439 Test Failures Later: An Empirical Evaluation of Flaky Failure Classifiers',
      'Abdulrahman Alshammari; Paul Ammann; Michael Hilton; Jonathan Bell', 2024,
      'https://arxiv.org/abs/2401.15788', 'EXCLUDE',
      'EC5: Phân loại flaky/real failures từ tests hiện có, không phải sinh JUnit bằng ChatGPT/Gemini.',
      'Title/abstract screening. Có thể tham khảo nền flaky detection ngoài evidence chính.')

paper(21, 'No More Manual Tests? Evaluating and Improving ChatGPT for Unit Test Generation',
      'Zhiqiang Yuan; Yiling Lou; Mingwei Liu; Shiji Ding; Kaixin Wang; Yixuan Chen; Xin Peng', 2024,
      'https://arxiv.org/html/2305.04207v3', 'INCLUDE',
      'IC1-IC5: Java unit tests do ChatGPT sinh, đo compile/pass và phân tích lỗi; ChatTester repair, đủ full-text method.',
      'CORE; supplemental citation/title discovery. Preprint đầu 2023; đọc v3 sửa 2024, journal title Evaluating and Improving ChatGPT for Unit Test Generation, DOI 10.1145/3660783.',
      source='sources/chattester_v3.html', location='Sections 3-5; Table 2; correctness analysis; ChatTester design; validity',
      tool='ChatGPT gpt-3.5-turbo; ChatTester; EvoSuite baseline',
      dataset='1,000 Java focal methods from 185 projects; additional 100 focal methods for ChatTester',
      setting='Basic context prompt; compile and execute generated tests; manually classify errors; iterative context enrichment and feedback repair',
      metric='Generated-test compilation rate and successful execution rate; readability/usability; coverage',
      result='Table 2: ChatGPT compiles 42.1% and passes 24.8% of 1,000 generated tests; EvoSuite 97.6% and 91.4%. Common compile issues include symbols/types/access; execution includes assertion failures.',
      code='Reported artifact: https://github.com/FudanSELab/ChatTester (chưa chạy tái lập)',
      limits='ChatTester repair is iterative, not one compiler repair. No Gemini/HumanEval. Human evaluation concerns passing-test readability/usability, not a paired human compile/pass baseline; sample differs for ChatTester.',
      relevance='CORE / high priority: metric definitions, compiler/runtime failure taxonomy and feedback repair; no direct evidence on the group exact task categories.',
      unit='generated test for one focal method', denominator='1,000 initial generated tests; separate 100-method ChatTester evaluation',
      repair='Iterative refinement with compiler/context feedback; multiple rounds', quality='MEDIUM; model/version and dataset external-validity limits')

paper(22, 'ChatUniTest: A Framework for LLM-Based Test Generation',
      'Yinghao Chen; Zehao Hu; Chen Zhi; Junxiao Han; Shuiguang Deng; Jianwei Yin', 2024,
      'https://arxiv.org/html/2305.04764v2', 'INCLUDE',
      'IC1-IC5: Framework sinh Java tests có validate/repair, đánh giá coverage, đủ model/dataset và full text.',
      'METHOD SUPPORT; supplemental citation/title discovery. v2 May 2024 / FSE demo; preprint đầu 2023 có title/authors khác, không trộn metadata.',
      source='sources/chatunitest.html', location='Framework generation/validation/repair; evaluation configuration and coverage table',
      tool='ChatUniTest; gpt-3.5-turbo-0613; TestSpark / EvoSuite baselines',
      dataset='4 Java projects (Commons CLI, Commons CSV, ecommerce, Binance); 264 sampled focal methods out of 835',
      setting='Adaptive context; syntax/compile/runtime validation; rule-based and LLM repair; default one generation with up to five repair attempts per round',
      metric='Line coverage; validation/repair architecture; no aggregate compile/pass rate table',
      result='Overall line coverage 59.6% vs TestSpark 42.1% and EvoSuite 38.2%; full text describes syntax, compilation and execution validation.',
      code='Reported artifact: https://github.com/ZJU-ACES-ISE/ChatUniTest (chưa chạy tái lập)',
      limits='Coverage differs from compilation/execution success; no HumanEval/Gemini/human paired baseline; multiple repairs. Demo-scale study.',
      relevance='METHOD SUPPORT: structured context and compiler/runtime validators; do not cite coverage as pass rate.',
      unit='sampled focal method / generated tests for coverage', denominator='264 sampled focal methods; no aggregate compile-and-run denominator reported',
      repair='Default up to five repairs per generation round', quality='MEDIUM; demo paper; outcome mismatch')

CANDIDATE_FIELDS = ['paper_id','title','authors','year','doi_or_url','decision','reason','notes']
EVIDENCE_FIELDS = ['paper_id','citation','database','tool_llm','dataset','setting','metric','main_result','code_available','limitations','rq_relevance']
LOG_FIELDS = ['database','query','date','raw_hits','screened','candidate','included','notes']

def upsert(path, fields, rows, key):
    existing = []
    if path.exists():
        with path.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != fields:
                raise ValueError(f'Unexpected schema: {path}: {reader.fieldnames}')
            existing = list(reader)
    newkeys = {key(row) for row in rows}
    retained = [row for row in existing if key(row) not in newkeys]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(retained + rows)

upsert(HERE/'candidate_papers.csv', CANDIDATE_FIELDS, papers, lambda r:r['paper_id'])
included = [p for p in papers if p['decision']=='INCLUDE']
evidence = []
for p in included:
    evidence.append(dict(paper_id=p['paper_id'],
        citation=f"{p['authors']} ({p['year']}). {p['title']}. {p['doi_or_url']}",
        database='Screenshot seed + primary-source verification' if int(p['paper_id'][-3:])<=20 else 'Supplementary citation/title discovery + arXiv full-text verification',
        tool_llm=p['tool'], dataset=p['dataset'], setting=p['setting'], metric=p['metric'],
        main_result=p['result'], code_available=p['code'], limitations=p['limits'], rq_relevance=p['relevance']))
upsert(ROOT/'team-synthesis/evidence_table.csv', EVIDENCE_FIELDS, evidence, lambda r:r['paper_id'])

logs = [
 dict(database='Semantic Scholar', query=QUERY, date=DATE, raw_hits='', screened=0, candidate=0, included=0,
      notes='KHOA batch; BLOCKED_HTTP_429. Public Graph API returned HTTP 429; public search/browser attempts did not yield an accessible result list. Blank raw_hits = unknown, not zero hits. No database results screened. sources/retrieval_log.json.'),
 dict(database='Google Scholar', query=QUERY, date=DATE, raw_hits='', screened=0, candidate=0, included=0,
      notes='KHOA batch; BLOCKED_HTTP_429. Shared query attempted on Scholar; HTTP 429 / browser inaccessible. Blank raw_hits = unknown. No database results screened. sources/retrieval_log.json.'),
 dict(database='User screenshot seed', query='20 paper-title entries in user image; exact-title primary-source verification (see title_verification_log.csv)', date=DATE,
      raw_hits=20, screened=20, candidate=11, included=9,
      notes='KHOA batch; raw_hits here means 20 supplied entries, not a search-engine estimate. 1 duplicate EC3 + 8 scope exclusions; 19 unique seed papers. candidate=11 retained for full-text assessment: 9 included after full text + 2 pending. Sources are publisher/arXiv/institutional records, not retrieved Semantic Scholar/Google Scholar results.'),
 dict(database='Supplementary citation/title discovery', query='"No More Manual Tests? Evaluating and Improving ChatGPT for Unit Test Generation"; "ChatUniTest: A Framework for LLM-Based Test Generation"', date=DATE,
      raw_hits=2, screened=2, candidate=2, included=2,
      notes='KHOA batch; targeted follow-up to repair/context references, verified against arXiv full text. raw_hits=2 retrieved unique candidate records, not total web search results. Does not replace the blocked shared database search.'),
]
upsert(HERE/'search_log.csv', LOG_FIELDS, logs, lambda r:(r['database'],r['query'],r['date']))
shared_logs = [dict(member='Nguyễn Nam Khoa', **r) for r in logs]
upsert(ROOT/'team-synthesis/search_log.csv', ['member']+LOG_FIELDS, shared_logs,
       lambda r:(r['member'],r['database'],r['query'],r['date']))

AUDIT_FIELDS = ['paper_id','date','origin','screening_stage','fulltext_status','fulltext_file','read_location','IC1','IC2','IC3','IC4','IC5','decision','primary_reason','metric_unit','denominator','repair_budget','reporting_quality','notes']
audit = []
for p in papers:
    yes = p['decision']=='INCLUDE'
    pending = p['decision']=='PENDING_FULL_TEXT'
    duplicate = p['paper_id']=='KHOA-014'
    audit.append(dict(paper_id=p['paper_id'],date=DATE,
       origin='User screenshot' if int(p['paper_id'][-3:])<=20 else 'Supplementary citation/title discovery',
       screening_stage='FULL_TEXT' if yes else 'FULL_TEXT_PENDING' if pending else 'DEDUPLICATION' if duplicate else 'TITLE_ABSTRACT',
       fulltext_status='READ' if yes else 'NOT_RETRIEVED' if pending else 'NOT_REQUIRED_AFTER_EARLY_EXCLUSION',
       fulltext_file=p.get('source',''), read_location=p.get('location','Title/abstract or duplicate identity'),
       IC1='PASS' if yes else 'PROVISIONAL' if pending else 'NOT_FULLTEXT_ASSESSED',
       IC2='PASS' if yes else 'UNCONFIRMED' if pending else 'NOT_FULLTEXT_ASSESSED',
       IC3='PASS_WITH_REPORTING_LIMITATIONS' if p['paper_id']=='KHOA-016' else 'PASS' if yes else 'UNCONFIRMED' if pending else 'NOT_FULLTEXT_ASSESSED',
       IC4='PASS' if yes else 'UNRESOLVED' if pending else 'NOT_FULLTEXT_ASSESSED',
       IC5='PASS' if yes else 'PROVISIONAL' if pending else 'NOT_FULLTEXT_ASSESSED',
       decision=p['decision'],primary_reason=p['reason'],metric_unit=p.get('unit',''),denominator=p.get('denominator',''),
       repair_budget=p.get('repair',''),reporting_quality=p.get('quality','NOT_FULLTEXT_ASSESSED'),notes=p['notes']))
upsert(HERE/'fulltext_screening.csv', AUDIT_FIELDS, audit, lambda r:r['paper_id'])

TITLE_FIELDS=['paper_id','source','query','date','raw_hits','verified_record_url','status','notes']
title_rows = []
for p in papers:
    title_rows.append(dict(paper_id=p['paper_id'],source='Title-based lookup / primary record verification',
       query='"'+p['title']+'"',date=DATE,raw_hits='',verified_record_url=p['doi_or_url'],
       status='DUPLICATE_NO_NEW_SEARCH' if p['paper_id']=='KHOA-014' else 'SECONDARY_METADATA_ONLY' if p['paper_id']=='KHOA-010' else 'PRIMARY_RECORD_VERIFIED',
       notes='Query column is the normalized title lookup string for reproducibility, not a verbatim archive of every web-tool query variant. Known candidate/title verification, not a shared-query database result. Search-engine total unavailable; blank is unknown. '+p['notes']))
upsert(HERE/'title_verification_log.csv',TITLE_FIELDS,title_rows,lambda r:r['paper_id'])

counts=Counter(p['decision'] for p in papers)
assert counts=={'INCLUDE':11,'EXCLUDE':9,'PENDING_FULL_TEXT':2}, counts
assert len({p['paper_id'] for p in papers})==22
assert {p['paper_id'] for p in evidence}=={p['paper_id'] for p in included}
assert all((HERE/p['source']).is_file() for p in included)

table=[]
for p in papers:
    label={'INCLUDE':'Giữ','EXCLUDE':'Loại','PENDING_FULL_TEXT':'Chờ toàn văn'}[p['decision']]
    table.append(f"| {p['paper_id']} | [{p['title']}]({p['doi_or_url']}) | {label} | {p['reason']} |")

report='''# Kết quả sàng lọc paper của Nguyễn Nam Khoa

Ngày tìm/đọc và ghi nhận: **09/10/2026**, múi giờ Asia/Saigon. Áp dụng query và IC/EC trong [protocol chung](../../team-synthesis/review_protocol.md) và [tiêu chí chung](../../team-synthesis/ie_criteria.md). Không sửa protocol của nhóm.

## Kết quả và phạm vi

Đã xử lý **20 mục trong ảnh**, bổ sung **2 paper về ChatTester/ChatUniTest**, tổng **22 records**. Sau bỏ một mục LM2Alloy bị lặp còn **21 paper độc lập**. Kết quả: **11 giữ**, **9 mục loại (1 trùng + 8 ngoài phạm vi)**, **2 chờ toàn văn**. Bảng evidence chung đã được điền 11 rows với mã `KHOA-*`; các mức CORE / METHOD SUPPORT / SUPPORTING / LOW_CONFIDENCE được ghi rõ, không xem cả 11 paper là bằng chứng trực tiếp ngang nhau.

**Giới hạn tìm kiếm:** Semantic Scholar (nguồn chính) và Google Scholar (bổ sung) đã được thử bằng query chung nhưng không trả danh sách kết quả truy cập được; các lần tải công khai trả HTTP 429. Vì vậy raw_hits của hai lượt này để trống, screened/candidate/included là 0 cho riêng các lượt bị chặn. Đây là kết quả sàng lọc danh sách gợi ý và tìm bổ sung có mục tiêu, **chưa phải một SLR đầy đủ từ hai cơ sở dữ liệu**. Không suy diễn '0 kết quả' từ lỗi truy cập.

```text
'''+QUERY+'''
```

Query trên giữ nguyên các toán tử của nhóm. Dấu ngoặc bao ngoài trong khối hiển thị chỉ để trình bày; query chính xác gửi khi truy cập nằm trong search_log.csv và retrieval_log.json.

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
'''+'\n'.join(table)+'''

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
'''
# Display the exact query without adding an outer grouping.
report=report.replace('('+QUERY+' )',QUERY).replace('Query trên giữ nguyên các toán tử của nhóm. Dấu ngoặc bao ngoài trong khối hiển thị chỉ để trình bày; query chính xác gửi khi truy cập nằm trong search_log.csv và retrieval_log.json.', 'Query trên giữ nguyên chuỗi của nhóm; bản gửi khi truy cập nằm trong search_log.csv và retrieval_log.json.')
(HERE/'screening_report.md').write_text(report,encoding='utf-8')

source_table=[]
for p in included:
    source_table.append(f"| {p['paper_id']} | [{p['source'].removeprefix('sources/')}]({p['source'].removeprefix('sources/')}) | [{p['title']}]({p['doi_or_url']}) | {p['location']} |")
source_readme='''# Sources for Khoa screening batch — 2026-10-09

Snapshots are retained for reading/audit, not a redistribution claim. Date: 2026-10-09, Asia/Saigon. Machine-readable URLs, response statuses and snapshot filenames: [retrieval_log.json](retrieval_log.json). HTML/PDF text was extracted locally; PDF result pages were rendered and visually checked in `qa/`.

| ID | Local full text | Primary citation / version URL | Read locations |
|---|---|---|---|
'''+'\n'.join(source_table)+'''

The unversioned ChatUniTest HTML snapshot contains v2 (2024). Paper metadata and results use that version, not the different v1 author list/title. ChatTester uses v3 (2024 revision of the 2023 preprint). TestART uses v6 (2025 revision of the 2024 preprint).

`chaining_ieee.html` and `llm_test_publisher.html` are publisher viewer pages, not the research full texts: use their `*_fulltext.pdf` files. `repair_ieee.html` is empty after HTTP 202 and **is not an accessible full text**. `failmapper_github.json` records artifact inventory, not a paper PDF. Do not count viewer/artifact/empty responses as satisfying IC4.

Semantic Scholar and Google Scholar requests returned HTTP 429; no result-list export exists. Search totals remain unknown. The supplied screenshot is a seed list of 20 title entries, recorded separately from search-engine results in the screening report. Title-based checks are supplementary verification, not database shared-query searches. The title-verification CSV supplies normalized title lookup strings; verbatim variants of web-tool search queries were not fully archived.
'''
(HERE/'sources/README.md').write_text(source_readme,encoding='utf-8')

# Structural validation of saved deliverables, including preserved shared schemas.
for path, fields in [(HERE/'candidate_papers.csv',CANDIDATE_FIELDS),
                     (HERE/'search_log.csv',LOG_FIELDS),
                     (ROOT/'team-synthesis/search_log.csv',['member']+LOG_FIELDS),
                     (ROOT/'team-synthesis/evidence_table.csv',EVIDENCE_FIELDS),
                     (HERE/'fulltext_screening.csv',AUDIT_FIELDS),
                     (HERE/'title_verification_log.csv',TITLE_FIELDS)]:
    with path.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        assert reader.fieldnames==fields, path
        rows=list(reader)
        assert all(None not in r and all(v is not None for v in r.values()) for r in rows), path
        if 'paper_id' in fields:
            assert len({r['paper_id'] for r in rows})==len(rows), path
print(json.dumps({'date':DATE,'records':len(papers),'unique_papers':21,'decisions':dict(counts),'evidence_rows_added':len(evidence),'database_search_status':'BLOCKED_HTTP_429; raw hit counts unknown'},ensure_ascii=False))
