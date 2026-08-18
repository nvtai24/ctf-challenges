# ✂️ Off By One

**Thể loại (Category):** Pwn

## 📖 Bối cảnh (Context)
Một đoạn mã C viết thủ công hàm sao chép chuỗi với độ an toàn cực cao. Nó khai báo bộ đệm 64 bytes và chạy vòng lặp sao chép từng ký tự. Vòng lặp điều kiện được viết là: `for (int i = 0; i <= 64; i++)`.

Nhìn qua có vẻ an toàn vì nó giới hạn độ dài, nhưng một con bọ nhỏ đang ẩn mình trong dấu `=`. Nó cho phép sao chép đúng 65 ký tự vào bộ đệm 64 bytes.

## 🎯 Mục tiêu (Objective)
- **Nhiệm vụ:** Tận dụng đúng 1 byte dư thừa đó để phá vỡ luồng chương trình.
- **Vấn đề / Lỗ hổng:** **Off-By-One Error**. Một byte thừa (thường là một byte rác hoặc `\x00`) tuy nhỏ, nhưng nếu nó ghi đè lên byte thấp nhất của con trỏ Saved EBP/RBP trên Stack, nó có thể làm sai lệch địa chỉ khôi phục khung (Frame Pointer), khiến hàm khi trả về (return) sẽ nhảy tới một vùng nhớ sai lệch do người chơi kiểm soát. Hoặc trên vùng nhớ Heap, một byte ghi đè Metadata của Chunk kế tiếp đủ sức làm sụp đổ hệ thống quản lý Heap.
- **Flag:** Biến đổi luồng thực thi để gọi hàm in ra Flag.

## 💡 Gợi ý (Hints)
- Nếu ghi đè một byte vào EBP, EBP sẽ bị kéo dịch về phía các biến cục bộ (vùng mà bạn có thể kiểm soát dữ liệu).
- Đây là kỹ thuật Stack Pivoting ở mức độ cơ bản.
