# Thử thách 07: HiddenAdmin - Giải pháp

## Loại lỗ hổng
**Broken Access Control / Insecure Direct Object Reference (Kiểm soát truy cập hỏng / Giả mạo tham số)**

## Mô tả
Ứng dụng kiểm tra vai trò (role) của người dùng thông qua tham số trên URL thay vì lấy từ Session ở phía server. Điều này cho phép người dùng nâng quyền (privilege escalation) dễ dàng bằng cách thao tác (tamper) tham số URL.

## Mã nguồn chứa lỗ hổng
```jsp
<%
  String role = request.getParameter("role");
  if(role == null) role = (String) session.getAttribute("role");
  // ...
  if("admin".equals(role)){ 
    // Hiện cờ (Flag)
  }
%>
```

## Khai thác (Exploit)

1. Đăng nhập bằng tài khoản: `staff` / `staff2024`
2. Bạn sẽ được chuyển hướng tới `dashboard.jsp` với tư cách là nhân viên.
3. Chú ý đoạn code kiểm tra vai trò từ tham số URL trước khi kiểm tra trong session.
4. Thêm tham số `?role=admin` vào URL: `/dashboard.jsp?role=admin`
5. Ứng dụng sẽ hiển thị giao diện dành cho quản trị viên và đi kèm với Flag.

## URL trực tiếp
```
http://[host]/dashboard.jsp?role=admin
```

## Flag
```
FCTF{r0l3_param_byp4ss_ez}
```

## Cách hoạt động
- Đầu tiên, đoạn mã lấy giá trị từ `request.getParameter("role")` (tham số truyền qua URL).
- Chỉ khi giá trị này bị `null` (không được truyền) thì nó mới fallback sang lấy giá trị `session.getAttribute("role")` an toàn trên server.
- Lỗ hổng logic này cho phép bất kỳ ai ghi đè vai trò của họ thông qua URL.

## Biện pháp phòng ngừa (Mitigation)
- Không bao giờ tin tưởng dữ liệu do client cung cấp (như param, cookie, header) khi đưa ra quyết định phân quyền (Authorization).
- Luôn sử dụng Session được quản lý phía server để lưu và kiểm tra quyền hạn:
  ```jsp
  String role = (String) session.getAttribute("role");
  // Không đọc request.getParameter đối với các dữ liệu mang tính phân quyền
  ```
- Triển khai Access Control chuẩn chỉnh.
- Sử dụng các security framework phổ biến (như Spring Security, Apache Shiro).
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
