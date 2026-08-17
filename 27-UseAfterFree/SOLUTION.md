# Thử thách 27: UseAfterFree - Giải pháp

## Mô tả
Một thử thách khai thác Use-After-Free (UAF) kinh điển trên Heap. Chương trình cho phép bạn phân bổ (allocate) các Ghi chú (Notes), giải phóng (free) chúng, và phân bổ một vé Admin (AdminTicket).

## Lỗ hổng
Khi một Ghi chú được giải phóng bằng `free()` (Tùy chọn 2), con trỏ (pointer) trỏ tới nó trong danh sách mảng `notes` KHÔNG bị xóa bỏ (không gán bằng NULL). Điều này để lại một **con trỏ lơ lửng (Dangling Pointer)**.

Khi một đối tượng mới (như `AdminTicket`) được cấp phát sau đó, bộ quản lý bộ nhớ `malloc` sẽ tận dụng lại chính vùng nhớ (chunk) vừa mới được giải phóng kia để tiết kiệm không gian.
Bởi vì chúng ta vẫn còn giữ một con trỏ trỏ thẳng vào vùng nhớ này (chính là con trỏ của Ghi chú cũ), chúng ta hoàn toàn có thể ra lệnh "đọc Ghi chú" để ép chương trình in ra các thuộc tính bí mật nằm bên trong `AdminTicket`!

## Khai thác (Exploit)
1. Kết nối vào máy chủ qua TCP (`nc <ip> <port>`).
2. Tạo Ghi chú mới (Tùy chọn `1`) với nội dung bất kỳ. Ghi chú này sẽ được cấp phát tại chunk có chỉ mục (index) là `0`.
3. Giải phóng Ghi chú `0` (Tùy chọn `2`). Vùng nhớ được trả lại cho Heap, nhưng con trỏ `0` vẫn còn tồn tại.
4. Yêu cầu cấp vé Admin (Tùy chọn `4`). Hành động này sẽ yêu cầu một vùng nhớ mới, và malloc sẽ tái sử dụng lại chunk `0` vừa được giải phóng.
5. Đọc Ghi chú `0` (Tùy chọn `3`). Chương trình sẽ ngây thơ lấy dữ liệu tại vùng nhớ `0` (lúc này thực chất đang chứa đối tượng `AdminTicket`) và ép kiểu nó thành chuỗi văn bản (Note). Lỗi nhầm lẫn kiểu dữ liệu (Type Confusion) này sẽ trực tiếp làm rò rỉ Flag!

## Flag
```
FCTF{u4f_d4ngl1ng_p01nt3r_1s_b4d}
```
