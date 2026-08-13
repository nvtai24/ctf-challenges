# 30 - Ret2Libc

## Description
A simulation of a modern "Ret2Libc" exploit bypassing ASLR (Address Space Layout Randomization).
The challenge dynamically randomizes the base address of `libc` every time you connect, just like a real system with ASLR. 

## Vulnerability
The program kindly prints the memory address of `puts()`. Since the offset of `puts()` inside `libc` is known (and provided), we can calculate the `libc` base address. 
Once we have the base address, we can calculate the real memory addresses of `system()` and the `'/bin/sh'` string. 
Then, a standard buffer overflow lets us construct a ROP chain to call `system('/bin/sh')`.

## Exploit (Python `pwntools` concept)
The challenge requires us to parse the leaked `puts` address and generate a payload dynamically, so a python script is usually used.

Let's assume the leak prints: `puts() is currently loaded at: 0x7f12345809c0`
1. Calculate Base: `Base = 0x7f12345809c0 - 0x0809c0 = 0x7f1234500000`
2. Calculate System: `System = Base + 0x04f440 = 0x7f123454f440`
3. Calculate /bin/sh: `Binsh = Base + 0x1b3e9a = 0x7f12346b3e9a`
4. Construct ROP Chain:
   - `40 bytes` of padding (32 buffer + 8 rbp)
   - `pop rdi; ret;` (`0x401234`)
   - `Binsh` address
   - `System` address

Because the address changes every time, you would normally write a script to connect, parse the output, calculate the hex string, and send it back. 

To solve this manually to test, you can connect, note the address, do the math quickly or use a python interactive shell, generate the hex payload, and paste it.

**Flag:** `FCTF{r3t2l1bc_4slr_byp4ss_m4st3r}`
