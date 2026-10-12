# Ứng viên paper 01: sàng lọc sơ bộ

- **Bài báo:** Mohammed Latif Siddiq và cộng sự, *Using Large Language Models to Generate JUnit Tests: An Empirical Study*, EASE 2024. DOI: https://doi.org/10.1145/3661167.3661216
- **Bản toàn văn của tác giả:** https://s2e-lab.github.io/preprints/ease24-preprint.pdf
- **Mức sàng lọc:** `candidate` sau khi xem tiêu đề, tóm tắt và phương pháp; **chưa** đánh dấu `included`.
- **Lý do giữ làm ứng viên:** Bài báo tạo JUnit 5 bằng mô hình ngôn ngữ trên bản Java của HumanEval và đo tỷ lệ biên dịch. Điều này gần với dữ liệu và chỉ số chính trong RQ của nhóm.
- **Minh họa khi demo:** Bảng 1 của bài báo báo cáo 43,1% bộ test GPT-3.5-Turbo trên HumanEval biên dịch được trước khi sửa bằng heuristic; sau sửa là 81,3%. Đây là số liệu **của bài báo**, không phải kết quả thực nghiệm của nhóm.
- **Giới hạn:** Bài báo không thử Gemini, và sửa bằng heuristic khác quy trình một vòng phản hồi trình biên dịch của nhóm. Cần đánh giá toàn văn và kiểm tra trùng trước khi đưa vào tổng quan chính thức.
- **Nguồn tìm:** Tìm thử trên web để xác định bài báo có DOI ACM. Chưa chạy chuỗi tìm kiếm chung trực tiếp trong ACM Digital Library; chưa có tổng số kết quả (`raw_hits`).
- **Bỏ trùng:** Đã kiểm tra các CSV paper hiện có trong repo; chưa thấy DOI `10.1145/3661167.3661216`. Khóa bỏ trùng dùng trong `RQ_01_all_records.csv` là `doi:10.1145/3661167.3661216`.

**Việc tiếp theo của An:** chạy chuỗi tìm kiếm chung trên ACM Digital Library, ghi số kết quả và tiếp tục sàng lọc nhiều paper. Bản ghi này chỉ là một bước khởi đầu cho ngày 2–3, chưa đủ yêu cầu của cả nhóm.
