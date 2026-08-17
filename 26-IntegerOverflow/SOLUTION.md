# Thử thách 26: IntegerOverflow - Giải pháp

## Mô tả
Thử thách này mô phỏng một lỗ hổng logic nghiệp vụ kinh điển phát sinh do hiện tượng Tràn số nguyên (Integer Overflow) trên kiểu biến số nguyên có dấu 32-bit (Signed 32-bit Integer) trong C. Bạn có khởi điểm là $100, nhưng FLAG lại có giá $1,000,000. Liệu bạn có thể hack sập hệ thống thanh toán của cửa hàng để mua được nó không?

## Lỗ hổng
Hệ thống tính tổng tiền bằng công thức `total = qty * price` (Tổng tiền = số lượng x đơn giá). Với kiểu số nguyên có dấu 32-bit (Signed 32-bit Integer), giá trị dương tối đa là `2147483647` (`0x7FFFFFFF`). Nếu tổng tiền vượt qua ngưỡng này, nó sẽ bị tràn (wrap around) và biến thành một **con số âm** khổng lồ.

Bởi vì `total` lúc này bị lật thành số âm, hệ thống kiểm tra số dư `if (total <= balance)` sẽ cho qua ngon ơ (vì một số âm luôn nhỏ hơn số dư 100 của bạn). Sau đó, câu lệnh trừ tiền `balance -= total` thực chất lại là trừ đi một số âm (Âm với Âm thành Cộng), vô tình nạp thêm một núi tiền khổng lồ vào tài khoản của bạn!

## Khai thác (Exploit)
1. Kết nối tới server qua TCP (`nc <ip> <port>`).
2. Chọn mua bình máu (Health Potion) có đơn giá: $10.
3. Số nguyên dương 32-bit lớn nhất là `2147483647`. Chúng ta cần tính toán số lượng mua sao cho `qty * 10 > 2147483647`.
4. Lựa chọn mua `214748365` bình máu: `214748365 * 10 = 2147483650`.
5. Trong không gian Signed 32-bit, con số `2147483650` sẽ bị tràn và biến thành `-2147483646`.
6. Nhập số lượng cần mua: `214748365`.
7. Tổng chi phí bị tính thành `$-2147483646`. Mua hàng thành công, và số dư (Balance) của bạn đột nhiên tăng vọt lên thành `$2147483746`.
8. Lúc này bạn đã thành tỷ phú, hãy thoải mái mua Flag!

## Flag
```
FCTF{1nt3g3r_0v3rfl0w_m4k3s_y0u_r1ch}
```
