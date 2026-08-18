# Thử thách 35: Zip In Zip - Giải pháp

## Loại lỗ hổng
**Lập trình kịch bản (Scripting) & Misc**

## Mô tả
Thử thách yêu cầu ứng dụng kỹ năng viết Script tự động hóa để giải quyết các công việc lặp đi lặp lại nhàm chán. File `flag_archives.zip` chứa `level_48.zip`, bên trong lại chứa `level_47.zip`,... cho đến khi ra file chứa cờ.

## Các bước thực hiện (Exploit)
1. Đặt file zip vào một thư mục trống và viết script `solve.py`:
   ```python
   import zipfile, os

   current_zip = "flag_archives.zip"
   while True:
       try:
           with zipfile.ZipFile(current_zip, 'r') as zip_ref:
               zip_ref.extractall(".")
               extracted_files = zip_ref.namelist()
           os.remove(current_zip)  # Xóa file cũ cho gọn
           if len(extracted_files) > 0 and extracted_files[0].endswith('.zip'):
               current_zip = extracted_files[0]
           else:
               print("Extracted final file:", extracted_files[0])
               break
       except Exception as e:
           print("Lỗi:", e)
           break
   ```
2. Chạy script. Nó sẽ tự động bung nén 50 lần và để lại file `flag.txt`.
3. Đọc nội dung file `flag.txt` để lấy cờ.

## 🚩 Cờ (Flag)
```
FLAG{z1p_b0mbs_4r3_4nn0y1ng}
```

## Biện pháp phòng ngừa (Mitigation)
- Kỹ thuật nén nhiều lớp thường được lợi dụng để tạo Zip Bomb nhằm gây tấn công từ chối dịch vụ (DoS) cạn kiệt tài nguyên máy chủ. Hệ thống giải nén cần giới hạn số lớp đệ quy (recursion limit) và kích thước tệp đầu ra tối đa.
