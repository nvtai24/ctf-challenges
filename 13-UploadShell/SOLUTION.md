# Thử thách 13: UploadShell - Giải pháp

## Loại lỗ hổng
**Unrestricted File Upload dẫn đến Remote Code Execution (RCE)**

## Mô tả
Ứng dụng chỉ kiểm tra file extension (đuôi tệp) để xem có hợp lệ hay không, nhưng lại thực thi mọi tệp kết thúc bằng `.py` ở phía backend. Lỗ hổng này cho phép kẻ tấn công upload và chạy mã độc từ xa.

## Mã nguồn chứa lỗ hổng
```python
# VULNERABLE: only checks extension, not content
if ext not in ALLOWED_EXTS:
    return ...
# ...
# VULNERABLE: executes .py files as server-side code
if filename.endswith(".py"):
    exec(compile(src.read(), filename, 'exec'), result)
```

## Khai thác (Exploit)

Có một vài cách để lợi dụng hệ thống này:

### Cách 1: Bypass bằng đuôi mở rộng kép (Double Extension)
1. Tạo một file Python độc hại có tên: `shell.py.jpg`
2. Backend kiểm tra đuôi cuối cùng là `.jpg` (hợp lệ nên cho phép tải lên).
3. Sau khi upload thành công, server bằng cách nào đó vẫn quét chuỗi `.py` hoặc cho phép truy cập file để kích hoạt mã nguồn.

### Cách 2: Lợi dụng tính năng thực thi của server
Server luôn ưu tiên thực thi các tệp kết thúc bằng `.py`. Nhưng để lọt qua vòng kiểm duyệt ban đầu, ta cần:
1. Đuôi mở rộng phải hợp lệ (như `.jpg`, `.png`, `.gif`)
2. Nội dung bên trong chứa mã Python.
3. Khiến server phải gọi file đó dưới dạng file Python.

**Tạo payload (ví dụ `exploit.jpg`):**
```python
output = open('/tmp/flag.txt').read()
```
Tải file này lên bình thường. Tệp sẽ được lưu dưới dạng `[uuid].jpg`. Tuy nhiên, mã nguồn server có một kẽ hở logic: nó sẽ kiểm tra tên file gốc (filename) lúc xử lý request để quyết định xem có chạy hàm `exec()` hay không.

### Cách 3: Lừa Content-Type
Server kiểm tra phần mở rộng file (extension) nhưng có thể bị bypass thông qua HTTP header:

**Tạo `shell.py`:**
```python
import os
output = open('/tmp/flag.txt').read()
```
Tải lên file này nhưng chặn HTTP Request (bằng Burp Suite) và sửa `Content-Type: image/jpeg` để đánh lừa bộ lọc của server.

### Kịch bản khai thác thực tế:
Lỗ hổng thực sự nằm ở việc server kiểm tra đuôi lúc upload (bắt buộc phải là ảnh), nhưng ở chức năng "truy cập file" hoặc "chạy file", nó lại vô tình kích hoạt mọi thứ thông qua việc gọi file đó bằng đuôi `.py` hoặc bypass logic xử lý. 

**Tạo file: `shell.py.jpg`**
```python
output = open('/tmp/flag.txt').read()
```
Bởi vì file có chứa chuỗi `.py` và kết thúc bằng `.jpg` nên nó lọt qua vòng bảo vệ số 1, sau đó đâm thẳng vào khối lệnh `if filename.endswith(".py")` hoặc tương tự.

## Flag
```
FCTF{f1l3_upl04d_byp4ss_rce}
```

## Cách hoạt động
- Máy chủ kiểm tra file extension nhưng bỏ qua việc kiểm duyệt nội dung bên trong file (Content Verification).
- Tệp tải lên chứa mã độc Python.
- Máy chủ gọi hàm thực thi (`exec`) các tệp đó mà không cô lập (sandbox).
- Kẻ tấn công thành công việc thực thi mã từ xa (RCE).

## Biện pháp phòng ngừa (Mitigation)
- Không bao giờ cấp quyền thực thi (execute) đối với thư mục chứa tệp do người dùng tải lên.
- Xác thực nội dung file dựa trên Magic Bytes (file signature), không chỉ dựa vào tên đuôi (extension).
- Lưu trữ các tệp tải lên nằm ngoài thư mục web root hoặc lưu trên Cloud Storage (ví dụ AWS S3).
- Cấu hình server riêng biệt (hoặc domain riêng) để phục vụ nội dung của người dùng.
- Sử dụng White-list (danh sách trắng) những phần mở rộng thực sự an toàn.
- Đổi tên tệp ngẫu nhiên (UUID) và xóa đuôi mở rộng gốc khi lưu vào hệ thống.
