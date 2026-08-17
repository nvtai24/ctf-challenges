# Thử thách 09: RobotsSecret - Giải pháp

## Loại lỗ hổng
**Information Disclosure (Tiết lộ thông tin) qua tệp robots.txt**

## Mô tả
Tệp `robots.txt` của ứng dụng làm lộ các đường dẫn ẩn và những endpoint nhạy cảm, vô tình đóng vai trò như một bản đồ giúp hacker điều hướng hệ thống.

## Mã nguồn chứa lỗ hổng
```python
@app.route("/robots.txt")
def robots():
    # Leaks hidden admin path
    return "User-agent: *\nDisallow: /admin-panel\nDisallow: /user/1\nDisallow: /backup/\n"
```

## Khai thác (Exploit)

1. Truy cập vào `/robots.txt`.
2. Nội dung file tiết lộ:
   ```text
   User-agent: *
   Disallow: /admin-panel
   Disallow: /user/1
   Disallow: /backup/
   ```
3. Dòng `Disallow: /user/1` cho thấy có một tài khoản người dùng nhạy cảm được giấu kín.
4. Truy cập đường dẫn: `/user/1`
5. Trang này tiết lộ hồ sơ quản trị viên (Alice) và hiển thị Flag.

## URL trực tiếp
```
http://[host]/user/1
```

## Flag
```
FCTF{r0b0ts_l34k_s3cr3ts}
```

## Cách hoạt động
- `robots.txt` được dùng để báo cho các công cụ tìm kiếm (như Google) biết không nên lập chỉ mục (crawl) các trang nào.
- Tuy nhiên, tệp này luôn có thể truy cập công khai (public).
- Hacker thường xuyên xem tệp `robots.txt` ở bước do thám (Reconnaissance) để tìm các điểm mù bảo mật.
- Việc khai báo các đường dẫn nhạy cảm vào đây chẳng khác nào vẽ đường cho hươu chạy.

## Biện pháp phòng ngừa (Mitigation)
- Không dùng `robots.txt` như một biện pháp bảo mật (Security by Obscurity - Bảo mật bằng cách che giấu là một phương pháp tồi).
- Không liệt kê danh sách các đường dẫn quản trị nhạy cảm vào `robots.txt`.
- Đảm bảo các endpoint nhạy cảm được bảo vệ bằng cơ chế phân quyền (Authentication & Authorization):
  ```python
  @app.route("/user/<uid>")
  def user(uid):
      if not is_authorized(uid):
          abort(403)
  ```
- Cân nhắc trả về HTTP Header `X-Robots-Tag: noindex` cho từng trang ẩn cụ thể thay vì gom vào file `robots.txt`.
