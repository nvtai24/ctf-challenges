# 29 - OffByOne

## Description
A simulation of a classic "poison null byte" / Off-By-One vulnerability. A vulnerable string copy function appends a null terminator outside the bounds of the 32-byte buffer.

## Vulnerability
The buffer is 32 bytes long, and immediately after it on the stack lies the `saved RBP` (Base Pointer). By writing exactly 32 bytes, the automatic null terminator (`\x00`) will overwrite the least significant byte of the `saved RBP`.
Original RBP: `0x7FFF00000130`
Corrupted RBP: `0x7FFF00000100`

Notice that `0x7FFF00000100` is exactly the address of our buffer! 
When the function returns, it executes `leave; ret;` (which is `mov rsp, rbp; pop rbp; ret`). Because `rbp` points to our buffer, `rsp` is moved to our buffer. The `pop rbp` instruction pops 8 bytes, moving `rsp` to `buffer + 8`. The `ret` instruction then pops the next 8 bytes (from `buffer + 8`) into the instruction pointer (`RIP`)!

## Exploit
To exploit this, our payload must be exactly 32 bytes long.
- Bytes 0-7: Dummy data (this will become the new RBP when popped)
- Bytes 8-15: The address of `win()` (this will be popped into RIP)
- Bytes 16-31: Padding to make the payload exactly 32 bytes.

**Addresses:**
`win()` = `0x401337`

**Payload construction (Little Endian):**
- Dummy (8 bytes): `4141414141414141`
- win() (8 bytes): `3713400000000000`
- Padding (16 bytes): `42424242424242424242424242424242`

Hex Payload:
`4141414141414141371340000000000042424242424242424242424242424242`

Send this hex string when prompted.

**Flag:** `FCTF{0ff_by_0n3_p1v0t_s74ck}`
