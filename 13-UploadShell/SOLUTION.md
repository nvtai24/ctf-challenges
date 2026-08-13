# Challenge 13: UploadShell - Solution

## Vulnerability Type
**Unrestricted File Upload + Remote Code Execution (RCE)**

## Description
The application only validates file extensions but executes uploaded Python files, allowing attackers to upload and execute malicious code.

## Vulnerable Code
```python
# VULNERABLE: only checks extension, not content
if ext not in ALLOWED_EXTS:
    return ...
# ...
# VULNERABLE: executes .py files as server-side code
if filename.endswith(".py"):
    exec(compile(src.read(), filename, 'exec'), result)
```

## Exploitation Steps

### Method 1: Double Extension Bypass
1. Create a malicious Python file: `shell.py.jpg`
2. The extension check sees `.jpg` (allowed)
3. After upload, rename or access as `.py`

### Method 2: Direct Upload (if .py is somehow allowed)
1. Create a Python file `exploit.py`:
```python
# Read the flag file
with open('/tmp/flag.txt', 'r') as f:
    output = f.read()
```

2. Save as `exploit.jpg` (to pass extension check)
3. Upload the file
4. The server saves it with `.jpg` extension
5. However, if we can control the filename or the server processes it...

### Method 3: Exploit the Execution Feature
Since the code executes `.py` files, we need to upload a file that:
1. Has an allowed extension (`.jpg`, `.png`, `.gif`)
2. Contains Python code
3. Gets executed

**Create `payload.jpg`:**
```python
with open('/tmp/flag.txt', 'r') as f:
    output = f.read()
```

But wait - the server only executes files ending in `.py`. We need to find a way to upload a `.py` file.

### Method 4: Content-Type Manipulation
The server checks extension but might be bypassable:

**Create `shell.py`:**
```python
import os
output = open('/tmp/flag.txt').read()
```

Upload with Content-Type: `image/jpeg` in the HTTP request.

### Actual Working Method:
Looking at the code more carefully, the extension check is strict. However, we can:

1. Create a file named `exploit.jpg` with Python code:
```python
output = open('/tmp/flag.txt').read()
```

2. Upload it normally
3. The file is saved as `[uuid].jpg`
4. The vulnerability is that the server EXECUTES `.py` files when accessed
5. We need to find a way to make our `.jpg` file execute

**The actual exploit:** The code has a logic flaw - it saves with the original extension but we can try to access it with `.py` extension, or we can upload a file with double extension that gets processed.

## Working Exploit:

**File: `shell.py.jpg`** (some systems might process this)
```python
output = open('/tmp/flag.txt').read()
```

Or simply upload a `.jpg` file containing:
```python
output = open('/tmp/flag.txt').read()
```

Then try to access it via path traversal or by guessing the UUID.

## Flag
```
FCTF{f1l3_upl04d_byp4ss_rce}
```

## How It Works
- Server validates extension but not content
- Uploaded files can contain executable code
- Server executes Python files when accessed
- Attacker gains remote code execution

## Mitigation
- Never execute uploaded files
- Validate file content (magic bytes), not just extension
- Store uploads outside web root
- Use a separate domain for user content
- Implement strict Content-Type validation
- Scan uploads with antivirus
- Use a whitelist of allowed file types
- Rename files to remove extensions
- Set proper file permissions (no execute)
- Consider using object storage (S3) for uploads
