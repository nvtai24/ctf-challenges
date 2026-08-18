# 📚 Return To Libc

**Thể loại (Category):** Pwn

## 📖 Bối cảnh (Context)
Một thử thách Pwnable kinh điển. Hệ thống bật NX (không cho chạy mã độc trên Stack) và bật cả ASLR (địa chỉ bộ nhớ thư viện thay đổi ngẫu nhiên sau mỗi lần chạy). File nhị phân bị lỗi Buffer Overflow, nhưng bên trong file hoàn toàn không chứa đoạn mã nào gọi hàm `system` hay có sẵn chuỗi `"/bin/sh"` để bạn ráp ROP Gadget.

Tất cả những gì hệ thống cung cấp là một file thư viện C chuẩn (`libc.so`).

## 🎯 Mục tiêu (Objective)
- **Nhiệm vụ:** Khai thác lỗi tràn bộ đệm để chiếm quyền shell, đánh bại cả bảo vệ NX và một phần ASLR.
- **Vấn đề / Lỗ hổng:** **Return-to-libc (ret2libc) kèm Information Leak**. Người chơi phải thực hiện khai thác 2 bước (2 stages). Bước 1: Dùng Buffer Overflow để hướng chương trình gọi một hàm xuất dữ liệu (như `puts`) để in ra địa chỉ bộ nhớ thật của một hàm thư viện đang chạy. Từ địa chỉ thật đó, trừ đi địa chỉ bù (Offset) trong file `libc.so` để tính ra "Base Address". Bước 2: Gọi quay ngược chương trình (ret2main), xây dựng payload lần 2 với địa chỉ thật của hàm `system` vừa tính toán được.
- **Flag:** Chiếm shell quyền cao nhất.

## 💡 Gợi ý (Hints)
- Công thức: `Libc Base = Leaked Address - Offset_of_leaked_func`.
- `System Address = Libc Base + Offset_of_system`.
- Dùng thư viện Python `pwntools` sẽ giúp bạn làm việc này dễ dàng hơn nhiều.
