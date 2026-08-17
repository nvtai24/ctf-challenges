# Thử thách 05: CookieMonster - Giải pháp

## Loại lỗ hổng
**Insecure Cookie Manipulation / Client-Side Security Control (Kiểm soát bảo mật qua Cookie thiếu an toàn)**

## Mô tả
Ứng dụng đang lưu trữ thông tin về vai trò (role) của người dùng bằng một cookie dưới dạng văn bản thuần túy (plain-text), không hề được mã hóa. Bất kỳ ai cũng có thể dễ dàng sửa đổi giá trị này ở phía client.

## Mã nguồn chứa lỗ hổng
```javascript
// VULNERABLE: role stored in plain cookie
res.cookie('username', 'guest');
res.cookie('role', 'guest');
```

## Khai thác (Exploit)

1. Đăng nhập bằng tài khoản: `guest` / `guest123`
2. Mở trình duyệt và bật Developer Tools (nhấn F12).
3. Chuyển sang tab Application (hoặc Storage) → mục Cookies.
4. Tìm cookie có tên `role` đang mang giá trị `guest`.
5. Chỉnh sửa giá trị của cookie này thành `admin`.
6. Tải lại trang (F5) hoặc truy cập trực tiếp vào `/dashboard`.
7. Hệ thống sẽ nhận diện bạn là quản trị viên.

## Payload thay thế (Dùng cURL)
```bash
curl -H "Cookie: username=guest; role=admin" http://[host]/dashboard
```

## Flag
```
FCTF{c00k13s_4r3_n0t_s3cr3ts}
```

## Biện pháp phòng ngừa (Mitigation)
- Không bao giờ lưu trữ các dữ liệu nhạy cảm (như vai trò, quyền hạn) trong cookie ở phía client.
- Nên dùng Session phía server để lưu trữ thông tin về trạng thái hoặc phân quyền của người dùng.
- Nếu bắt buộc phải lưu thông tin trong cookie, hãy mã hóa hoặc ký (sign) cookie bằng HMAC để ngăn chặn thay đổi trái phép.
- Triển khai Session một cách an toàn:
  ```javascript
  req.session.role = 'guest'; // Lưu vào Session phía server
  ```
- Sử dụng các token xác thực chuẩn (ví dụ: JWT được ký đầy đủ).
- Luôn bật các cờ bảo mật `HttpOnly` và `Secure` cho cookie.
