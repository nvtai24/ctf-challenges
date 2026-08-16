# 👋 SSTI Greet

## 📖 Bối cảnh (Context)
Dịch vụ tạo thiệp chúc mừng điện tử này dường như đã biết về lỗ hổng SSTI nên họ đã thiết lập một bộ lọc (Filter) rất gắt gao. Họ cấm các từ khóa nhạy cảm như `class`, `mro`, `subclasses`, `os`, `import`, và thậm chí cấm cả dấu ngoặc vuông `[` `]` hoặc dấu ngoặc kép.

Họ tin rằng như thế là đủ để khiến mọi cao thủ SSTI phải bó tay.

## 🎯 Mục tiêu (Objective)
- **Nhiệm vụ:** Tìm cách luồn lách qua bộ lọc chặn ký tự và từ khóa để leo thang đặc quyền, lấy được RCE.
- **Vấn đề / Lỗ hổng:** **Advanced SSTI & WAF Evasion**. Kẻ tấn công có thể sử dụng các phương pháp thay thế như: dùng `request.args` để truyền tên biến, dùng các bộ lọc built-in (như `|attr()`) thay cho dấu chấm hoặc ngoặc vuông, hoặc mã hóa từ khóa bằng định dạng Hex/Unicode.
- **Flag:** Đọc file Flag trên server.

## 💡 Gợi ý (Hints)
- Nếu `class` bị cấm, bạn có thể truyền nó qua tham số GET: `request.args.c` với `?c=__class__`.
- Dấu ngoặc vuông `[0]` có thể được thay thế bằng hàm lấy phần tử như `__getitem__(0)` hoặc `pop()`.
