# Challenge 09: RobotsSecret - Solution

## Vulnerability Type
**Information Disclosure via robots.txt**

## Description
The application's `robots.txt` file reveals hidden paths and sensitive endpoints that should not be publicly accessible.

## Vulnerable Code
```python
@app.route("/robots.txt")
def robots():
    # Leaks hidden admin path
    return "User-agent: *\nDisallow: /admin-panel\nDisallow: /user/1\nDisallow: /backup/\n"
```

## Exploitation Steps

1. Navigate to `/robots.txt`
2. The file reveals:
   ```
   User-agent: *
   Disallow: /admin-panel
   Disallow: /user/1
   Disallow: /backup/
   ```
3. The `Disallow: /user/1` line reveals a hidden user profile
4. Navigate to `/user/1`
5. This displays Alice's admin profile with the flag

## Direct URL
```
http://[host]/user/1
```

## Flag
```
FCTF{r0b0ts_l34k_s3cr3ts}
```

## How It Works
- `robots.txt` is meant to tell search engines which pages not to crawl
- However, it's publicly accessible and often reveals sensitive paths
- Attackers routinely check `robots.txt` for information disclosure
- The file acts as a roadmap to hidden or sensitive areas

## Mitigation
- Don't rely on `robots.txt` for security (it's not access control)
- Implement proper authentication and authorization
- Don't list sensitive paths in `robots.txt`
- Use proper access controls on sensitive endpoints:
  ```python
  @app.route("/user/<uid>")
  def user(uid):
      if not is_authorized(uid):
          abort(403)
  ```
- Consider using `X-Robots-Tag` header instead for specific pages
- Security through obscurity is not security
- Use authentication for all sensitive resources
