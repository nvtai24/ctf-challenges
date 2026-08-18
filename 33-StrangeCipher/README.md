# Thử thách 33: Strange Cipher

## 📖 Bối cảnh (Context)
Chúng tôi bắt được một đoạn mã hóa lạ nằm trong file `ciphertext.txt`, cùng với một đoạn script Python `encrypt.py` - dường như là thuật toán đã tạo ra nó. Khóa mã hóa đã bị giấu đi, hoặc có thể nó đã bị rò rỉ đâu đó trong mã nguồn. Hãy viết script giải mã để tìm lại cờ.

## 🎯 Mục tiêu (Objective)
- Tìm và giải mã thông tin ẩn để lấy cờ.
- Định dạng cờ: `FLAG{...}`

## 💡 Gợi ý (Hints)
- Đọc kỹ file `encrypt.py` để hiểu cách dữ liệu bị biến đổi.
- Phép toán XOR (`^`) có một tính chất rất đặc biệt: Nó có tính đối xứng. Nếu `A ^ B = C`, thì `C ^ B = A`.
- Điều đó có nghĩa là quá trình mã hóa và giải mã đối với phép XOR (khi biết khóa) là hoàn toàn giống hệt nhau!
