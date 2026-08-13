import os
import sys
import struct

FLAG = os.environ.get("FLAG", "FCTF{r0p_ch41n_m4st3r_g4dg3ts}")
BANNER = r"""
  ____   ___  ____    ____ _           _       
 |  _ \ / _ \|  _ \  / ___| |__   __ _(_)_ __  
 | |_) | | | | |_) | | |   | '_ \ / _` | | '_ \ 
 |  _ <| |_| |  __/  | |___| | | | (_| | | | | |
 |_| \_\\___/|_|      \____|_| |_|\__,_|_|_| |_|
  Binary Exploitation Lab
"""

# Gadgets and function addresses
POP_RDI_RET = 0x400010
POP_RSI_RET = 0x400020
BIN_SH_STR  = 0x400030
SYSTEM_ADDR = 0x400040

def main():
    print(BANNER)
    print("Welcome to the ROP training facility.")
    print("Can you chain the gadgets to execute system('/bin/sh', 0)?\n")
    
    print(f"[+] pop rdi; ret;    -> {hex(POP_RDI_RET)}")
    print(f"[+] pop rsi; ret;    -> {hex(POP_RSI_RET)}")
    print(f"[+] '/bin/sh' string -> {hex(BIN_SH_STR)}")
    print(f"[+] system()         -> {hex(SYSTEM_ADDR)}")
    print("\nBuffer is 32 bytes, followed by 8 bytes saved RBP, then the Return Address.")
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

    # Simulated Stack after overflow
    # offset 40 is the first return address
    stack = payload[40:]
    
    # Simulate CPU registers
    rdi = 0
    rsi = 0
    
    # Instruction pointer starts at the first overwritten return address
    ip_index = 0
    
    print("\n[+] Executing ROP chain...")
    while ip_index < len(stack):
        if ip_index + 8 > len(stack):
            print("[-] Segmentation fault (unaligned stack)")
            break
            
        ip = struct.unpack("<Q", stack[ip_index:ip_index+8])[0]
        ip_index += 8
        
        if ip == POP_RDI_RET:
            print("  -> Executing: pop rdi; ret;")
            if ip_index + 8 > len(stack):
                print("[-] Segmentation fault (stack empty during pop rdi)")
                break
            rdi = struct.unpack("<Q", stack[ip_index:ip_index+8])[0]
            ip_index += 8
            
        elif ip == POP_RSI_RET:
            print("  -> Executing: pop rsi; ret;")
            if ip_index + 8 > len(stack):
                print("[-] Segmentation fault (stack empty during pop rsi)")
                break
            rsi = struct.unpack("<Q", stack[ip_index:ip_index+8])[0]
            ip_index += 8
            
        elif ip == SYSTEM_ADDR:
            print(f"  -> Executing: system({hex(rdi)}, {hex(rsi)})")
            if rdi == BIN_SH_STR and rsi == 0:
                print(f"\n[!] Success! Shell spawned!")
                print(f"[*] FLAG: {FLAG}")
                sys.exit(0)
            else:
                print("[-] system() called with incorrect arguments!")
                print(f"    Expected: system({hex(BIN_SH_STR)}, 0x0)")
                sys.exit(1)
                
        else:
            print(f"[-] Segmentation fault (jump to invalid address: {hex(ip)})")
            sys.exit(1)
            
    print("\n[-] ROP chain ended without calling system()")
    
if __name__ == "__main__":
    main()
