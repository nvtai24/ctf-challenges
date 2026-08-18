# Thử thách 31: Hidden In Plain Sight - Giải pháp

## Loại lỗ hổng
**Steganography (Giấu tin cơ bản)**

## Mô tả
Thử thách này giới thiệu về kỹ thuật giấu tin (Steganography) thô sơ nhất: nối thêm (append) văn bản thuần túy (plaintext) vào cuối một file nhị phân (ví dụ như JPG hoặc PNG). Vì trình xem ảnh thường bỏ qua mọi dữ liệu sau ký hiệu kết thúc file (EOF), bức ảnh vẫn hiển thị bình thường nhưng lại mang theo dữ liệu ẩn.

## Các bước thực hiện (Exploit)
1. Tải file `secret_image.jpg` về máy tính.
2. Mở terminal (trên Linux hoặc WSL).
3. Chạy lệnh `strings secret_image.jpg` để trích xuất tất cả các chuỗi ký tự có thể đọc được từ file nhị phân này.
4. Do output có thể khá dài, hãy kết hợp với `grep` để lọc cờ: 
   ```bash
   strings secret_image.jpg | grep FLAG
   ```
5. Dòng cuối cùng của kết quả sẽ chứa cờ gốc.

## 🚩 Cờ (Flag)
```
FLAG{st3g0_1s_3asy_wh3n_1ts_1n_pl41n_s1ght}
```

## Biện pháp phòng ngừa (Mitigation)
- Đối với phân tích, hãy luôn kiểm tra dữ liệu rác (junk data) ở cuối file bằng các công cụ như `binwalk` hoặc `exiftool`.
- Khi xây dựng hệ thống upload ảnh, nên xử lý (re-encode) hoặc dọn dẹp ảnh bằng thư viện xử lý ảnh chuyên dụng (như ImageMagick hoặc Pillow) để loại bỏ metadata và dữ liệu thừa.
