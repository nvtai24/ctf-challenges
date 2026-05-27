# Challenge 10: ForgetMe - Solution

## Vulnerability Type
**Predictable Password Reset Token / Weak Token Generation**

## Description
The password reset tokens follow a predictable pattern (username + "2024"), allowing attackers to guess tokens and reset other users' passwords.

## Vulnerable Code
```javascript
// Predictable reset tokens: username + "2024"
const resetTokens = { alice: 'alice2024', bob: 'bob2024' };
```

## Exploitation Steps

1. Go to "Forgot password?" link
2. Enter username: `alice`
3. The system shows a partially masked token: `a****`
4. The hint mentions tokens follow a predictable pattern
5. Try common patterns: `alice2024`, `alice123`, etc.
6. The correct token is: `alice2024`
7. Enter token and set a new password
8. Login as alice with your new password
9. View the flag on the dashboard

## Token Pattern
```
Token = username + "2024"
```

## Flag
```
FCTF{br0k3n_p4ssw0rd_r3s3t}
```

## How It Works
- Reset tokens should be cryptographically random
- This implementation uses a simple, predictable formula
- Attacker can easily guess the token for any user
- No rate limiting or attempt tracking

## Mitigation
- Generate cryptographically secure random tokens:
  ```javascript
  const crypto = require('crypto');
  const token = crypto.randomBytes(32).toString('hex');
  ```
- Store tokens with expiration time in database
- Implement rate limiting on reset attempts
- Send tokens only via secure channel (email)
- Never display tokens in the UI (even partially)
- Invalidate token after use
- Add account lockout after multiple failed attempts
- Use time-based one-time passwords (TOTP) or similar
