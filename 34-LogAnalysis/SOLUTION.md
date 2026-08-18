# Thử thách 34: Log Analysis - Giải pháp

## Loại lỗ hổng
**Network Forensics & Data Exfiltration**

## Mô tả
Sau khi thực hiện một loạt các thao tác SQL Injection (`UNION SELECT`), hacker đã thu thập được dữ liệu và quyết định truyền dữ liệu đó ra ngoài (Exfiltration) thông qua phương thức GET request với mã hóa Base64.

## Các bước thực hiện (Exploit)
1. Mở file `access.log` bằng trình soạn thảo văn bản hoặc dùng lệnh `cat`/`less` trên Linux.
2. Quan sát phần lớn log là các payload dò tìm SQLi. Chú ý dòng log cuối cùng:
   ```
   192.168.1.5 - - [...] "GET /image.png?data=RkxBR3tuM3R3MHJrX3RyNGZmMWNfbjN2M3JfbDFzcz0= HTTP/1.1" 404 195
   ```
3. Tham số `data` chứa chuỗi `Rkx...=` kết thúc bằng dấu bằng `=`, là dấu hiệu nhận biết cực kỳ phổ biến của mã hóa Base64.
4. Sao chép đoạn mã đó và giải mã bằng [CyberChef](https://gchq.github.io/CyberChef/) (recipe: From Base64), hoặc dùng lệnh Linux: 
   ```bash
   echo "RkxBR3tuM3R3MHJrX3RyNGZmMWNfbjN2M3JfbDFzcz0=" | base64 -d
   ```
5. Bạn sẽ thu được cờ gốc.

## 🚩 Cờ (Flag)
```
FLAG{n3tw0rk_tr4ff1c_n3v3r_l13s}
```

## Biện pháp phòng ngừa (Mitigation)
- Cần thiết lập hệ thống cảnh báo (SIEM/WAF) để theo dõi các dấu hiệu tấn công SQLi (từ khóa `UNION`, `SELECT`, `OR 1=1`) và chặn đứng từ sớm.
- Giám sát các truy vấn có tham số URL dài bất thường hoặc chứa mã hóa Base64 đáng ngờ.
