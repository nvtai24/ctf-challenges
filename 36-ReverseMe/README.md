# Thử thách 36: Reverse Me

**Thể loại (Category):** Reverse Engineering

## 📖 Bối cảnh (Context)
Chúng tôi tìm thấy một ứng dụng xác thực nho nhỏ được viết bằng Python. Tuy nhiên, lập trình viên đã biên dịch nó sang định dạng bytecode `.pyc` nhằm mục đích che giấu mã nguồn. Hãy tìm cách dịch ngược (decompile) file `.pyc` này để khôi phục mã nguồn và lấy flag nhé.

## 🎯 Mục tiêu (Objective)
- Tìm và giải mã thông tin ẩn để lấy cờ.
- Định dạng cờ: `FLAG{...}`

## 💡 Gợi ý (Hints)
- `.pyc` là định dạng bytecode đã được biên dịch của Python, không phải là mã máy native thực sự (như `.exe`).
- Do đặc thù của Python, có những công cụ mạnh mẽ có thể khôi phục `.pyc` trở lại thành mã nguồn `.py` (gần như nguyên vẹn hoàn hảo).
- Thử tìm hiểu công cụ có tên là `uncompyle6` hoặc `decompyle3`, hoặc đơn giản là tìm các trang web "Decompile python online".
