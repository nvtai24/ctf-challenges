# Thử thách 34: Log Analysis

**Thể loại (Category):** Forensic

## 📖 Bối cảnh (Context)
Máy chủ web của chúng tôi đã bị tấn công vào rạng sáng nay. Đội ngũ an ninh đã trích xuất được file nhật ký truy cập `access.log`. Kẻ tấn công dường như đã sử dụng lỗ hổng SQL Injection và trích xuất thành công một thông tin bí mật. Bạn hãy phân tích file log để tìm lại thông tin đó nhé.

## 🎯 Mục tiêu (Objective)
- Tìm và giải mã thông tin ẩn để lấy cờ.
- Định dạng cờ: `FLAG{...}`

## 💡 Gợi ý (Hints)
- Kẻ tấn công thường gửi thông tin bí mật trích xuất được lên server của chính hắn, hoặc ghi nó vào các file, hoặc phản hồi qua HTTP param.
- Bạn có thấy tham số URL nào chứa một chuỗi ký tự nhìn giống Base64 không?
- Chú ý đến các request HTTP cuối cùng trong log.
