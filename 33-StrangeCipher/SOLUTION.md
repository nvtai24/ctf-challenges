# Thử thách 33: Strange Cipher - Giải pháp

## Loại lỗ hổng
**Cryptography (XOR Cipher)**

## Mô tả
Đây là bài tập Cryptography kinh điển về mã hóa XOR. File `encrypt.py` cho thấy từng ký tự của cờ (plaintext) đã bị đem XOR với từng ký tự tương ứng của một chuỗi khóa (key). Khóa `secret_key` đã bị để lại dưới dạng comment trong mã nguồn.

## Các bước thực hiện (Exploit)
1. Phân tích `encrypt.py`, ta thấy hàm mã hóa lặp qua chuỗi, áp dụng toán tử XOR (`^`) giữa ký tự và khóa `secret_key`.
2. Dựa vào tính đối xứng của XOR, hàm giải mã sẽ sử dụng *chính xác* vòng lặp và phép toán đó.
3. Viết script `decrypt.py`:
   ```python
   def xor_decrypt(ciphertext, key):
       res = []
       for i in range(len(ciphertext)):
           res.append(chr(ciphertext[i] ^ ord(key[i % len(key)])))
       return "".join(res)

   with open("ciphertext.txt", "rb") as f:
       cipher = f.read()
   print(xor_decrypt(cipher, "secret_key"))
   ```
4. Chạy script để thu được cờ gốc.

## 🚩 Cờ (Flag)
```
FLAG{x0r_c1ph3r_1s_w34k_but_fun}
```

## Biện pháp phòng ngừa (Mitigation)
- Tuyệt đối không sử dụng XOR thuần túy hoặc mật mã tự chế (Custom Cryptography) cho các dữ liệu quan trọng.
- Tránh hardcode khóa mã hóa (Encryption Key) trong mã nguồn ứng dụng.
- Sử dụng các tiêu chuẩn mã hóa mạnh như AES-GCM với các thư viện mã hóa chuẩn được công nhận.
