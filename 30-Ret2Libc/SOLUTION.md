# Thử thách 30: Ret2Libc - Giải pháp

## Mô tả
Thử thách này mô phỏng kỹ thuật khai thác **Return-to-libc (Ret2Libc)** hiện đại nhằm qua mặt cơ chế bảo vệ ASLR (Address Space Layout Randomization).
Để mô phỏng môi trường thực tế, hệ thống sẽ tự động chọn một địa chỉ cơ sở (Base Address) ngẫu nhiên cho thư viện `libc` mỗi lần bạn kết nối vào.

## Lỗ hổng
Chương trình đã rất "tốt bụng" khi chủ động in ra màn hình địa chỉ bộ nhớ hiện tại của hàm `puts()`. Bởi vì khoảng cách (Offset) cố định của hàm `puts()` bên trong thư viện `libc` là một hằng số đã biết trước (và được đề bài cho sẵn), chúng ta có thể làm toán trừ để tìm ra địa chỉ gốc (Base Address) của toàn bộ `libc`.

Khi đã nắm trong tay địa chỉ Base, chúng ta có thể dễ dàng tính toán ra địa chỉ thực tế trên bộ nhớ của hàm `system()` và cả chuỗi ký tự `'/bin/sh'` nằm bên trong libc.
Sau đó, chỉ cần lợi dụng lỗi Buffer Overflow tiêu chuẩn để nhồi một chuỗi ROP-chain nhằm gọi lệnh `system('/bin/sh')`.

## Khai thác (Bằng mã giả Python `pwntools`)
Vì địa chỉ thay đổi liên tục mỗi lần chạy, bạn không thể code cứng (hardcode) Payload được. Bắt buộc phải viết một script Python để tự động nhận chuỗi rò rỉ, làm toán, và sinh Payload động.

Giả sử chương trình in ra: `puts() is currently loaded at: 0x7f12345809c0`
1. **Tính Base Address:** `Base = 0x7f12345809c0 - 0x0809c0 = 0x7f1234500000`
2. **Tính địa chỉ system():** `System = Base + 0x04f440 = 0x7f123454f440`
3. **Tính địa chỉ /bin/sh:** `Binsh = Base + 0x1b3e9a = 0x7f12346b3e9a`
4. **Lắp ráp chuỗi ROP:**
   - Đệm rác `40 bytes` (Gồm 32 bytes buffer + 8 bytes saved RBP)
   - Địa chỉ Gadget `pop rdi; ret;` (Giả sử là `0x401234`)
   - Địa chỉ biến `Binsh` (Chui vào thanh ghi rdi)
   - Địa chỉ hàm `System` (Gọi system("/bin/sh"))

Trong môi trường CTF thực tế, bạn sẽ dùng thư viện `pwntools` để xử lý các bước socket, tính toán offset tĩnh (ELF) và đóng gói Little-Endian một cách tự động.
Nếu muốn làm bằng tay (Manual), bạn phải kết nối bằng Netcat, thao tác nhanh để copy địa chỉ, ném vào Python shell tính toán, dùng hàm `struct.pack` sinh chuỗi hex, rồi copy paste ngược lại terminal trước khi session bị timeout.

## Flag
```
FCTF{r3t2l1bc_4slr_byp4ss_m4st3r}
```
