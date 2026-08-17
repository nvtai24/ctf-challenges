# Thử thách 10: ForgetMe - Giải pháp

## Loại lỗ hổng
**Predictable Token / Insecure Randomness (Token dự đoán được / Sinh số ngẫu nhiên yếu)**

## Mô tả
Tính năng Đặt lại mật khẩu (Password Reset) sinh ra token theo một quy luật rất dễ dự đoán (tên người dùng + "2024"). Lỗ hổng logic này giúp kẻ tấn công (hacker) đoán được token của bất kỳ user nào và chiếm quyền kiểm soát (account takeover).

## Mã nguồn chứa lỗ hổng
```javascript
// Predictable reset tokens: username + "2024"
const resetTokens = { alice: 'alice2024', bob: 'bob2024' };
```

## Khai thác (Exploit)

1. Truy cập trang "Quên mật khẩu?" (Forgot Password).
2. Nhập username nạn nhân: `alice`.
3. Hệ thống trả về token bị che một phần: `a****`.
4. Một gợi ý nhỏ cho thấy token được sinh ra theo quy luật.
5. Thử các mẫu dễ đoán: `alice2024`, `alice123`, v.v.
6. Đoán thành công token chuẩn là: `alice2024`.
7. Dùng token đó ở form Đặt lại mật khẩu để đổi mật khẩu cho Alice.
8. Đăng nhập vào account Alice với mật khẩu mới.
9. Đọc Flag ở bảng điều khiển (dashboard).

## Mẫu Token (Token pattern)
```text
Token = username + "2024"
```

## Flag
```
FCTF{br0k3n_p4ssw0rd_r3s3t}
```

## Cách hoạt động
- Theo nguyên tắc, token đặt lại mật khẩu phải được sinh ngẫu nhiên an toàn (cryptographically secure).
- Việc sử dụng công thức ghép chuỗi thuần túy khiến entropy bằng 0.
- Do không có cơ chế giới hạn số lần thử (Rate Limit), attacker có thể brute-force tự do.

## Biện pháp phòng ngừa (Mitigation)
- Phải tạo token bằng các hàm băm an toàn về mặt mật mã (CSPRNG):
  ```javascript
  const crypto = require('crypto');
  const token = crypto.randomBytes(32).toString('hex');
  ```
- Lưu token vào cơ sở dữ liệu cùng với thời gian hết hạn (expiration time).
- Áp dụng Rate Limit (giới hạn số lần thử reset).
- Gửi token qua các kênh an toàn (như Email hoặc SMS OTP).
- Không bao giờ làm lộ mã token (dù chỉ một phần) trên giao diện Web (frontend).
- Hủy token lập tức sau 1 lần sử dụng.
- Khóa tài khoản sau N lần nhập sai token.
