# Thử thách 08: PriceTag - Giải pháp

## Loại lỗ hổng
**Price Manipulation / Client-Side Trust (Thao túng giá / Tin tưởng dữ liệu từ client)**

## Mô tả
Ứng dụng tin tưởng tuyệt đối vào giá trị giá tiền (price) được gửi lên từ form phía client. Điều này cho phép kẻ tấn công sửa đổi giá để mua các mặt hàng với giá tùy ý (thậm chí là $0).

## Mã nguồn chứa lỗ hổng
```javascript
// VULNERABLE: trusts client-supplied price
app.post('/buy', (req,res) => {
  const id = parseInt(req.body.id);
  const paid = parseFloat(req.body.price);
  // ... sử dụng biến 'paid' để thanh toán mà không đối chiếu lại giá trong database
```

## Khai thác (Exploit)

1. Bạn được cấp tài khoản bắt đầu với số dư $10.
2. Mục tiêu là mua FLAG TOKEN có giá $999.99.
3. Dùng Inspect Element (F12) để xem mã HTML của nút "Mua" tương ứng với FLAG TOKEN:
   ```html
   <input type="hidden" name="price" value="999.99">
   ```
4. Sửa thẻ input ẩn này, thay đổi thuộc tính `value` thành `0.01` hoặc `1.00`.
5. Bấm nút "Mua" - bạn sẽ mua được FLAG TOKEN với mức giá vừa sửa.
6. Vào trang "Thanh toán" để nhận Flag.

## Cách 1: Sử dụng DevTools của trình duyệt
1. Nhấp chuột phải vào nút "Mua" của FLAG TOKEN.
2. Chọn Inspect (Kiểm tra phần tử).
3. Tìm dòng `<input type="hidden" name="price" value="999.99">`.
4. Sửa giá trị thành `1.00`.
5. Bấm nút Mua trên giao diện.

## Cách 2: Đánh chặn (Intercept) bằng Burp Suite
Bắt HTTP Request lúc bấm nút Mua và sửa param:
```
POST /buy HTTP/1.1
...
id=4&price=0.01
```

## Flag
```
FCTF{pr1c3_t4mp3r1ng_ch34ts}
```

## Cách hoạt động
- Form mua hàng submit cả `id` và `price` lên server.
- Server tin vào giá trị `price` do client cung cấp thay vì tự truy vấn (lookup) lại giá trị thực từ cơ sở dữ liệu.
- Hacker có thể thoải mái thao túng tham số này.

## Biện pháp phòng ngừa (Mitigation)
- Không bao giờ tin tưởng vào mức giá hoặc số lượng tiền tệ do client gửi lên.
- Luôn truy vấn lại giá trị thực của sản phẩm ở phía backend:
  ```javascript
  const product = products.find(p => p.id === id);
  const actualPrice = product.price; // Lấy giá từ DB, không dùng req.body.price
  ```
- Chỉ nên yêu cầu client gửi ID sản phẩm (và có thể là số lượng).
- Áp dụng các bước xác thực tính vẹn toàn cho mọi giao dịch tài chính.
- Ghi log (audit) toàn bộ các thay đổi hoặc giao dịch có rủi ro.
