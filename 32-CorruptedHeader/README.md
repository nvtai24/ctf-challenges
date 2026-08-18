# Thử thách 32: Corrupted Header

**Thể loại (Category):** Forensic

## 📖 Bối cảnh (Context)
Chúng tôi thu được file ảnh `corrupted_image.png` từ máy tính của nghi phạm, nhưng có vẻ nó đã bị làm hỏng cố ý để không thể mở được. Trình xem ảnh báo lỗi định dạng không hợp lệ. Hãy khôi phục lại cấu trúc của file này để đọc nội dung bên trong.

## 🎯 Mục tiêu (Objective)
- Tìm và giải mã thông tin ẩn để lấy cờ.
- Định dạng cờ: `FLAG{...}`

## 💡 Gợi ý (Hints)
- Hệ điều hành và các phần mềm dựa vào phần 'Magic Bytes' (File Signatures) ở đầu file để nhận diện chính xác định dạng file, chứ không chỉ dựa vào phần đuôi (extension).
- Hãy tìm hiểu xem Magic Bytes chuẩn của một file PNG là gì.
- Dùng một Hex Editor (như HxD trên Windows hoặc `hexeditor` trên Linux) để kiểm tra và sửa lại các byte đầu tiên của file.
