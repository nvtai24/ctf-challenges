# Thử thách 32: Corrupted Header - Giải pháp

## Loại lỗ hổng
**Forensics (Sửa Magic Bytes)**

## Mô tả
Thử thách yêu cầu kiến thức cơ bản về File Signatures. Bất kỳ file PNG hợp lệ nào cũng bắt buộc phải bắt đầu bằng 8 byte đặc trưng `89 50 4E 47 0D 0A 1A 0A`. Kẻ gian đã ghi đè 8 byte này bằng các số 0, khiến phần mềm không thể đọc được.

## Các bước thực hiện (Exploit)
1. Mở file `corrupted_image.png` bằng một trình chỉnh sửa Hex (Hex Editor) như HxD.
2. Quan sát hàng đầu tiên, ta thấy 8 byte đầu tiên đang bị đổi thành `00 00 00 00 00 00 00 00`.
3. Ngay sau đó là chuỗi khối dữ liệu `IHDR` đặc trưng của PNG. Điều này khẳng định đây là file PNG bị hỏng header.
4. Sửa 8 byte đầu tiên thành Magic Bytes của chuẩn PNG: `89 50 4E 47 0D 0A 1A 0A`.
5. Lưu file lại.
6. Mở file ảnh vừa sửa bằng trình xem ảnh bình thường, bạn sẽ thấy cờ.

## 🚩 Cờ (Flag)
```
FLAG{m4g1c_byt3s_s4v3_th3_d4y}
```

## Biện pháp phòng ngừa (Mitigation)
- Trong quá trình thiết kế phần mềm, đừng bao giờ tin tưởng hoàn toàn vào đuôi file `.png` hay `.jpg`. Luôn kiểm tra File Signature để xác thực nội dung.
- Nắm vững cấu trúc file giúp kỹ sư điều tra số (Forensics) khôi phục được nhiều dữ liệu bị xóa hoặc phá hoại.
