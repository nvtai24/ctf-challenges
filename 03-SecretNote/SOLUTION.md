# Thử thách 03: SecretNote - Giải pháp

## Loại lỗ hổng
**Insecure Direct Object Reference (IDOR - Tham chiếu đối tượng trực tiếp không an toàn)**

## Mô tả
Ứng dụng không kiểm tra xem người dùng hiện tại có phải là chủ sở hữu của ghi chú (note) mà họ đang muốn truy cập hay không. Bất kỳ người dùng nào đã đăng nhập đều có thể xem ghi chú của người khác chỉ bằng cách thay đổi ID của ghi chú trên URL.

## Mã nguồn chứa lỗ hổng
```javascript
// VULNERABLE: no ownership check
app.get('/note/:id', (req, res) => {
  if (!req.session.user) return res.redirect('/');
  const note = notes[req.params.id];
  // ... hiển thị ghi chú nhưng không kiểm tra req.session.user.id === note.owner
```

## Khai thác (Exploit)

1. Đăng nhập bằng tài khoản: `bob` / `bob456`
2. Bạn sẽ thấy danh sách ghi chú của riêng mình (ID 1, 2, 5).
3. Mật khẩu của Admin nằm ở ghi chú số 3 (thuộc về user 1 - alice).
4. Sửa URL trực tiếp trên thanh địa chỉ thành: `/note/3`
5. Ứng dụng sẽ hiển thị nội dung ghi chú mà không kiểm tra quyền sở hữu.

## Truy cập URL trực tiếp
```
http://[host]/note/3
```

## Flag
```
FCTF{1d0r_1s_ev3rywh3r3}
```

## Biện pháp phòng ngừa (Mitigation)
- Luôn kiểm tra xem người dùng hiện tại có quyền truy cập vào tài nguyên được yêu cầu hay không.
- Thêm mã kiểm tra quyền sở hữu (ownership check):
  ```javascript
  if (note.owner !== req.session.user.id) {
    return res.status(403).send('Access denied');
  }
  ```
- Triển khai các biện pháp phân quyền (Authorization) chặt chẽ.
- Cân nhắc sử dụng Access Control List (ACL) hoặc Role-Based Access Control (RBAC).
