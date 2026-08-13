import os
import sys
import struct
import random

FLAG = os.environ.get("FLAG", "FCTF{r3t2l1bc_4slr_byp4ss_m4st3r}")
BANNER = r"""
  ____      _   ____  _     _ _          
 |  _ \ ___| |_|___ \| |   (_) |__   ___ 
 | |_) / _ \ __| __) | |   | | '_ \ / __|
 |  _ <  __/ |_ / __/| |___| | |_) | (__ 
 |_| \_\___|\__|_____|_____|_|_.__/ \___|
  Binary Exploitation Lab
"""

# "Libc" offsets
LIBC_PUTS_OFFSET   = 0x0809c0
LIBC_SYSTEM_OFFSET = 0x04f440
LIBC_BINSH_OFFSET  = 0x1b3e9a

# Simulated runtime addresses (ASLR is ON)
LIBC_BASE = random.randint(0x7F0000000000, 0x7FFFF0000000) & ~0xFFF

puts_addr   = LIBC_BASE + LIBC_PUTS_OFFSET
system_addr = LIBC_BASE + LIBC_SYSTEM_OFFSET
binsh_addr  = LIBC_BASE + LIBC_BINSH_OFFSET

POP_RDI_RET = 0x401234 # Static gadget in binary (No PIE for the main executable)

def main():
    print(BANNER)
    print("Welcome to Ret2Libc. ASLR is enabled.")
    print("You must bypass ASLR by leaking a libc address first, then exploiting a buffer overflow.\n")
    
    print("[+] Given libc offsets:")
    print(f"    puts   : {hex(LIBC_PUTS_OFFSET)}")
    print(f"    system : {hex(LIBC_SYSTEM_OFFSET)}")
    print(f"    /bin/sh: {hex(LIBC_BINSH_OFFSET)}")
    print(f"\n[+] Gadget in binary (No PIE):")
    print(f"    pop rdi; ret; -> {hex(POP_RDI_RET)}\n")
    
    print("--- Stage 1: Information Leak ---")
    print("The program conveniently prints the resolved address of puts() for you!")
    print(f"puts() is currently loaded at: {hex(puts_addr)}")
    
    print("\n--- Stage 2: Buffer Overflow ---")
    print("Buffer is 32 bytes, followed by 8 bytes saved RBP, then the Return Address.")
    print("Construct your ROP chain to call system('/bin/sh')")
    print("Provide your payload as hex:")
    sys.stdout.flush()
    
    try:
        raw = input("> ").strip()
        payload = bytes.fromhex(raw)
    except:
        print("\n[-] Disconnected")
        sys.exit(1)

    if len(payload) <= 40:
        print("[-] Payload too short to overwrite return address.")
        sys.exit(1)

    stack = payload[40:]
    ip_index = 0
    rdi = 0
    
    print("\n[+] Executing ROP chain...")
    while ip_index < len(stack):
        if ip_index + 8 > len(stack):
            break
            
        ip = struct.unpack("<Q", stack[ip_index:ip_index+8])[0]
        ip_index += 8
        
        if ip == POP_RDI_RET:
            if ip_index + 8 > len(stack):
                break
            rdi = struct.unpack("<Q", stack[ip_index:ip_index+8])[0]
            ip_index += 8
            
        elif ip == system_addr:
            if rdi == binsh_addr:
                print(f"\n[!] Success! Shell spawned!")
                print(f"[*] FLAG: {FLAG}")
                sys.exit(0)
            else:
                print(f"[-] system() called with incorrect argument (RDI: {hex(rdi)})")
                print(f"    Expected: {hex(binsh_addr)}")
                sys.exit(1)
                
        else:
            print(f"[-] Segmentation fault (jump to invalid address: {hex(ip)})")
            sys.exit(1)
            
    print("\n[-] ROP chain ended without calling system()")
    sys.exit(1)
    
if __name__ == "__main__":
    main()
