# Thử thách 35: Zip In Zip

**Thể loại (Category):** Misc

## 📖 Bối cảnh (Context)
Hacker đã giấu flag vào một file nén. Tuy nhiên, hắn quá rảnh rỗi nên đã nén file đó lại... 50 lần (theo kiểu búp bê Nga Russian Doll)! Việc giải nén từng file bằng tay có vẻ bất khả thi. Hãy dùng kỹ năng lập trình của bạn để giải nén tự động và lấy cờ.

## 🎯 Mục tiêu (Objective)
- Tìm và giải mã thông tin ẩn để lấy cờ.
- Định dạng cờ: `FLAG{...}`

## 💡 Gợi ý (Hints)
- Đừng cố gắng click giải nén bằng tay.
- Viết một script Python (sử dụng thư viện `zipfile` hoặc `shutil`), hoặc một shell script (sử dụng lệnh `unzip` trên Linux) để thực hiện giải nén tự động trong vòng lặp.
- Hãy chú ý xóa file zip cũ sau mỗi lần giải nén để tránh lộn xộn ổ cứng.
