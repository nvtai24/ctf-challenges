# Challenge 05: CookieMonster - Solution

## Vulnerability Type
**Insecure Cookie Manipulation / Client-Side Security Control**

## Description
The application stores the user's role in a plain, unencrypted cookie that can be easily modified by the client.

## Vulnerable Code
```javascript
// VULNERABLE: role stored in plain cookie
res.cookie('username', 'guest');
res.cookie('role', 'guest');
```

## Exploitation Steps

1. Login with credentials: `guest` / `guest123`
2. Open browser Developer Tools (F12)
3. Go to Application/Storage → Cookies
4. Find the `role` cookie with value `guest`
5. Edit the cookie value to `admin`
6. Refresh the page or navigate to `/dashboard`
7. The application now treats you as an admin

## Alternative Method (Using curl)
```bash
curl -H "Cookie: username=guest; role=admin" http://[host]/dashboard
```

## Flag
```
FCTF{c00k13s_4r3_n0t_s3cr3ts}
```

## Mitigation
- Never store sensitive data (like roles) in client-side cookies
- Use server-side sessions to store user roles
- If cookies must be used, sign them with HMAC or encrypt them
- Use secure session management:
  ```javascript
  req.session.role = 'guest'; // Store in server-side session
  ```
- Implement proper authentication tokens (JWT with signature)
- Set cookies with `httpOnly` and `secure` flags
