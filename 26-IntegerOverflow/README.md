# 🧮 Integer Overflow

**Thể loại (Category):** Pwn

## 📖 Bối cảnh (Context)
Một trò chơi RPG trực tuyến cho phép người chơi đổi tiền Vàng lấy Đá quý. Hệ thống quy định 1 Đá quý giá 100 Vàng. Số lượng Đá quý bạn muốn mua được lưu bằng biến số nguyên dương nhỏ (kiểu `short int` 16-bit, giá trị tối đa là 32767). 

Lập trình viên nghĩ rằng số lượng tối đa này đã là quá an toàn vì không ai có đủ tiền mua đến ngưỡng đó.

## 🎯 Mục tiêu (Objective)
- **Nhiệm vụ:** Mua một lượng Đá quý khổng lồ mà không phải tốn một đồng Vàng nào, thậm chí còn được cộng thêm tiền Vàng vào tài khoản.
- **Vấn đề / Lỗ hổng:** **Integer Overflow (Tràn số nguyên)**. Khi nhân số lượng Đá quý khổng lồ với giá (ví dụ $32768 * 100$), kết quả vượt quá khả năng lưu trữ của biến kiểu Signed Integer, khiến số bị cuộn vòng và trở thành một số âm. Do đó, hệ thống sẽ trừ đi một số âm vào tài khoản của bạn (tức là cộng thêm tiền).
- **Flag:** Trở thành người giàu nhất server.

## 💡 Gợi ý (Hints)
- Tìm hiểu giới hạn tối đa của các kiểu dữ liệu số nguyên trong ngôn ngữ lập trình C/C++.
- Nhập một số đủ lớn để phép nhân bị tràn về giá trị âm.
