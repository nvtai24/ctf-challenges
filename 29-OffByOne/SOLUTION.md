# Thử thách 29: OffByOne - Giải pháp

## Mô tả
Mô phỏng lỗ hổng **Poison Null Byte** / **Off-By-One** cổ điển. Một hàm sao chép chuỗi bị lỗi đã vô tình chèn thêm ký tự null terminator (`\x00`) kết thúc chuỗi vượt ra ngoài biên giới của một buffer 32-byte (tức là ghi lố 1 byte).

## Lỗ hổng
Buffer có kích thước chính xác 32 bytes, và nằm ngay phía trên nó trên Stack chính là thanh ghi `Saved RBP` (Base Pointer). Bằng cách nhập vào một chuỗi đúng 32 ký tự, ký tự null (`\x00`) kết thúc chuỗi sẽ bị tràn và ghi đè thẳng vào byte có trọng số thấp nhất (Least Significant Byte) của `Saved RBP`.

Ví dụ:
- RBP gốc đang chứa: `0x7FFF00000130`
- RBP sau khi bị hỏng (Null-byte ghi đè số 30): `0x7FFF00000100`

Hãy để ý rằng `0x7FFF00000100` bây giờ đã vô tình trỏ thẳng vào **vị trí bắt đầu của Buffer chúng ta**!
Khi hàm thực thi xong và gọi lệnh trả về `leave; ret;` (bản chất của lệnh này là `mov rsp, rbp; pop rbp; ret`). 
Bởi vì `rbp` đang bị hỏng và trỏ vào buffer của chúng ta, lệnh đầu tiên sẽ kéo `rsp` xuống buffer. Lệnh `pop rbp` tiếp theo sẽ bật 8 byte đầu tiên vứt đi, kéo `rsp` thụt xuống `buffer + 8`. Cuối cùng, lệnh `ret` định mệnh sẽ lấy 8 byte tiếp theo trên ngăn xếp (tức là `buffer + 8`) nhét thẳng vào con trỏ lệnh `RIP`!

## Khai thác (Exploit)
Để kích hoạt được chuỗi logic này (hay còn gọi là kỹ thuật Stack Pivoting), Payload của chúng ta phải dài chính xác 32 bytes:
- **Bytes 0-7:** Dữ liệu rác (phần này sẽ bị pop vứt đi thành RBP mới).
- **Bytes 8-15:** Địa chỉ của hàm `win()` (phần này sẽ bị `ret` pop thẳng vào thanh ghi RIP).
- **Bytes 16-31:** Các byte rác để lấp đầy phần còn lại sao cho đủ độ dài chính xác là 32 bytes (Kích hoạt Off-by-one).

**Địa chỉ hàm mục tiêu:**
`win()` = `0x401337`

**Xây dựng tải trọng (Dạng Little Endian):**
- Rác (8 bytes): `4141414141414141`
- `win()` (8 bytes): `3713400000000000`
- Đệm lấp đầy (16 bytes): `42424242424242424242424242424242`

Chuỗi Payload Hexadecimal hoàn chỉnh:
`4141414141414141371340000000000042424242424242424242424242424242`

Gửi chuỗi Hex này khi được hỏi.

## Flag
```
FCTF{0ff_by_0n3_p1v0t_s74ck}
```
