# Thử thách 31: Hidden In Plain Sight

**Thể loại (Category):** Forensic

## 📖 Bối cảnh (Context)
Bức ảnh này trông có vẻ bình thường, nhưng một hacker đã giấu một thông điệp bí mật bên trong nó. Các kỹ thuật viên pháp y đã khẳng định rằng kích thước file có vẻ lớn hơn một chút so với bình thường. Bạn có thể tìm thấy nó không?

## 🎯 Mục tiêu (Objective)
- Tìm và giải mã thông tin ẩn để lấy cờ.
- Định dạng cờ: `FLAG{...}`

## 💡 Gợi ý (Hints)
- Có nhiều cách để giấu dữ liệu vào ảnh (Steganography).
- Cách đơn giản và thô sơ nhất là ghi trực tiếp thêm dữ liệu văn bản vào cuối luồng byte của file.
- Hãy thử dùng công cụ đọc các chuỗi ký tự (strings) được hỗ trợ mặc định trên Linux hoặc các công cụ phân tích Hex.
