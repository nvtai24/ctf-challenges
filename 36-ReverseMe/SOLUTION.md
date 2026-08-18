# Thử thách 36: Reverse Me - Giải pháp

## Loại lỗ hổng
**Dịch ngược Python (Reverse Engineering)**

## Mô tả
Thử thách này minh họa một sai lầm phổ biến: cho rằng việc biên dịch mã Python thành `.pyc` hoặc đóng gói thành `.exe` bằng PyInstaller có thể bảo vệ được tài sản trí tuệ (source code) hay các bí mật được hardcode.

## Các bước thực hiện (Exploit)
1. Tải file `checker.pyc` về.
2. **Cách 1 (Dùng công cụ web):** Truy cập một trang web dịch ngược python online (ví dụ: [pylingual.io](https://pylingual.io/) hoặc `toolnb.com/tools/pyc.html`), tải file lên và xem kết quả decompile.
3. **Cách 2 (Dùng command line):** Cài đặt công cụ `uncompyle6` bằng lệnh `pip install uncompyle6`.
4. Chạy lệnh: `uncompyle6 checker.pyc`
5. Kết quả in ra màn hình sẽ trả lại mã nguồn gốc của chương trình Python, trong đó có một biến hằng số tên là `SECRET_FLAG` chứa nguyên văn cờ cần tìm.

## 🚩 Cờ (Flag)
```
FLAG{pyth0n_byt3c0d3_r3v3rs1ng}
```

## Biện pháp phòng ngừa (Mitigation)
- Không bao giờ hardcode (gắn cứng) mật khẩu, token, khóa bí mật hay Flag trực tiếp vào mã nguồn.
- Biên dịch Python thành `.pyc` hoặc đóng gói bằng công cụ phổ thông không cung cấp bất kỳ biện pháp bảo mật nào để chống dịch ngược (Reverse Engineering). Cần sử dụng mã hóa phân mảnh (obfuscator) mã nguồn nếu thực sự cần bảo vệ code.
