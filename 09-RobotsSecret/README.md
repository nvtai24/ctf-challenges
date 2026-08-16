# 🤖 Robots Secret

## 📖 Bối cảnh (Context)
Một nhóm tin tặc mũ xám đang chia sẻ tài liệu mật trên một website ẩn danh. Để ngăn chặn các công cụ tìm kiếm (như Google, Bing) tự động thu thập và hiển thị các tài liệu nhạy cảm này trên kết quả tìm kiếm, họ đã thiết lập các quy tắc rất nghiêm ngặt nhằm hướng dẫn các con bot thu thập dữ liệu (Crawler) không được phép truy cập vào các thư mục chứa dữ liệu mật.

## 🎯 Mục tiêu (Objective)
- **Nhiệm vụ:** Tìm ra nơi nhóm tin tặc này giấu Flag trên website.
- **Vấn đề / Lỗ hổng:** **Information Disclosure qua file `robots.txt`**. File `robots.txt` vốn được sinh ra để chỉ định các thư mục cấm bot truy cập (Disallow), nhưng vì nó là file công khai, con người hoàn toàn có thể đọc được nó và vô tình biết được chính xác các đường dẫn bí mật mà quản trị viên đang muốn giấu.
- **Flag:** Nằm trong thư mục bị cấm trong file cấu hình bot.

## 💡 Gợi ý (Hints)
- File quy định quyền truy cập cho crawler thường được đặt ở ngay thư mục gốc của domain (ví dụ `http://example.com/robots.txt`).
- Hãy truy cập file đó và xem có đường dẫn nào lạ không.
