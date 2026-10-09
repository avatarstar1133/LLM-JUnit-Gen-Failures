# Demo thu thập metadata ACM bằng Python

## Chạy demo ngắn

Nhấp đúp `demo_acm.cmd`, hoặc chạy từ thư mục gốc dự án nếu đã cài Python:

```powershell
python ho-le-thien-an/SLR/search_acm.py --demo
```

Demo đọc lại metadata thật đã lưu ngày 09/10/2026, xử lý trong thư mục tạm: lần đầu thêm 20 candidate, lần hai thêm 0 vì trùng. Demo không truy cập mạng và không thay đổi CSV nghiên cứu.

## Kết quả hiện có

- Truy vấn chung trên ACM Full-Text Collection: **611 kết quả hiển thị**.
- Thu thập **20 bản ghi trang đầu**, chưa thu thập hết 611 kết quả.
- `candidate_papers.csv`: 20 bản ghi ứng viên của nguồn ACM.
- `../../RQ_01_all_records.csv`: đã thêm 20 bản ghi, trạng thái `candidate`.
- `search_log.csv`: ngày, truy vấn, tổng số kết quả, `screened=0`, `included=0`.
- `raw/acm_2026-10-09_page1.json`: metadata nguồn, URL truy vấn, thứ tự kết quả và cách thu thập.
- `raw/dedup_2ba4817c7f71.json`: đối chiếu 2 paper có DOI xuất hiện trong dữ liệu thành viên khác. Bản ghi theo từng nguồn vẫn giữ ở folder cá nhân; file chung chỉ có một dòng cho mỗi DOI khi nhập.

**Cách thu thập thực tế:** trang ACM công khai truy cập được bằng trình duyệt. Python HTTP trực tiếp nhận lỗi 403, nên lượt này lấy metadata hiển thị qua trình duyệt rồi đưa cho Python chuẩn hóa, bỏ trùng và ghi CSV. Đây là thu thập có công cụ hỗ trợ, không phải lượt tìm thủ công của An. Danh sách tác giả lấy theo hiển thị tìm kiếm, có thể bị rút gọn; năm lấy từ ngày hiển thị trên kết quả. Chưa đọc toàn văn hoặc quyết định paper đáp ứng IC/EC.

## Nói với cô trong 30 giây

> “Em chuẩn bị công cụ Python xử lý metadata từ ACM. Truy vấn hiện trả về 611 kết quả; em demo xử lý 20 bản ghi trang đầu đã thu qua trình duyệt. Công cụ lưu dữ liệu nguồn, chuẩn hóa DOI, phát hiện trùng và xuất CSV ứng viên. Chạy lại không tạo dòng trùng. Phần đọc và sàng lọc nội dung chưa hoàn thành, nên chưa có bài nào được đánh dấu included.”

## Các hàm cần giải thích

| Hàm | Nhiệm vụ |
|---|---|
| `crawl()` | Thử tải trang đầu ACM bằng HTTP; dừng và báo lỗi nếu bị 401/403/429. |
| `parse_search_html()` | Trích metadata và số kết quả từ trang HTML đã lưu. |
| `normalize_doi()` / `record_keys()` | Chuẩn hóa DOI và tạo khóa đối chiếu tên bài/năm. |
| `save_candidates()` | Ghi file cá nhân, file chung và search log; kiểm tra trùng trước khi ghi. |

## Thu thập lần sau

Chạy `--crawl --query "<truy vấn thực tế>"` khi ACM cho phép HTTP trực tiếp. Trên máy này cách đó đã bị 403; không xem lỗi này là kết quả tìm kiếm rỗng.

Nếu bị chặn HTTP, tự mở kết quả trong trình duyệt, lưu trang HTML (Ctrl+S), rồi nhập:

```powershell
python ho-le-thien-an/SLR/search_acm.py --html "duong-dan-trang-da-luu.html" --source-url "URL-tim-kiem-ACM" --date "YYYY-MM-DD"
```

Hoặc nhập lại snapshot hiện có (không tạo bản ghi trùng):

```powershell
python ho-le-thien-an/SLR/search_acm.py --snapshot ho-le-thien-an/SLR/raw/acm_2026-10-09_page1.json
```

Việc đã thu metadata không thay thế yêu cầu cá nhân tự đọc và sàng lọc mà giảng viên giao.
