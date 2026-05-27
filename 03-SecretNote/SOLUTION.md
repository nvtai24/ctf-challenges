# Challenge 03: SecretNote - Solution

## Vulnerability Type
**Insecure Direct Object Reference (IDOR)**

## Description
The application fails to verify that the logged-in user owns the note they're trying to access. Any authenticated user can view any note by manipulating the note ID in the URL.

## Vulnerable Code
```javascript
// VULNERABLE: no ownership check
app.get('/note/:id', (req, res) => {
  if (!req.session.user) return res.redirect('/');
  const note = notes[req.params.id];
  // ... displays note without checking if req.session.user.id === note.owner
```

## Exploitation Steps

1. Login with credentials: `bob` / `bob456`
2. You'll see your own notes (IDs 1, 2, 5)
3. The admin's secret note is ID 3 (owned by user 1 - alice)
4. Manually navigate to: `/note/3`
5. The application displays the note without checking ownership

## Direct URL
```
http://[host]/note/3
```

## Flag
```
FCTF{1d0r_1s_ev3rywh3r3}
```

## Mitigation
- Always verify that the authenticated user has permission to access the requested resource
- Add ownership check:
  ```javascript
  if (note.owner !== req.session.user.id) {
    return res.status(403).send('Access denied');
  }
  ```
- Implement proper authorization checks
- Use access control lists (ACLs) or role-based access control (RBAC)
