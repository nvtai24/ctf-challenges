import os
import sys
import struct

FLAG = os.environ.get("FLAG", "FCTF{0ff_by_0n3_p1v0t_s74ck}")
BANNER = r"""
  ___  __  __   ____         ___            
 / _ \|  \/  | | __ ) _   _ / _ \ _ __   ___ 
| | | | |\/| | |  _ \| | | | | | | '_ \ / _ \
| |_| | |  | | | |_) | |_| | |_| | | | |  __/
 \___/|_|  |_| |____/ \__, |\___/|_| |_|\___|
                      |___/                  
  Binary Exploitation Lab
"""

WIN_ADDR = 0x401337

def main():
    print(BANNER)
    print("Welcome to the Off-By-One (Poison Null Byte) lab.")
    print("A buggy strncpy() copies exactly N bytes, but always appends a null byte.")
    print("This allows overwriting the least significant byte (LSB) of the saved RBP.\n")
    
    # Original stack layout
    buffer_addr = 0x7FFF00000100
    original_rbp = 0x7FFF00000130
    
    # Since we overwrite the LSB with 0x00, the new RBP will be:
    # 0x7FFF00000100! (Which points exactly to our buffer!)
    
    print(f"[+] buffer address : {hex(buffer_addr)}")
    print(f"[+] original RBP   : {hex(original_rbp)}")
    print(f"[+] win() address  : {hex(WIN_ADDR)}")
    print("\n[!] If we write exactly 32 bytes to the 32-byte buffer, the null terminator")
    print("    will overwrite the lowest byte of the saved RBP at offset 32.")
    print("    This makes RBP point to our buffer when the function returns.")
    print("\nProvide your payload as hex:")
    sys.stdout.flush()
    
    try:
        raw = input("> ").strip()
        payload = bytes.fromhex(raw)
    except:
        print("\n[-] Disconnected")
        sys.exit(1)

    if len(payload) > 32:
        print("[-] Payload too large. Buffer is 32 bytes max.")
        sys.exit(1)
        
    # Pad payload to 32 bytes if they entered less
    buffer_content = payload.ljust(32, b"A")
    
    # Simulate the off-by-one
    saved_rbp_bytes = bytearray(struct.pack("<Q", original_rbp))
    if len(payload) == 32:
        # Off-by-one null byte overwrite!
        saved_rbp_bytes[0] = 0x00
        print("[!] Off-by-one triggered! Null byte appended at offset 32.")
    
    corrupted_rbp = struct.unpack("<Q", saved_rbp_bytes)[0]
    print(f"[+] Saved RBP is now : {hex(corrupted_rbp)}")
    sys.stdout.flush()
    
    if corrupted_rbp != original_rbp:
        print("[+] Stack pivot successful!")
        
        # When the caller returns, it executes `leave; ret;`
        # `leave` is `mov rsp, rbp; pop rbp`
        # If RBP points to our buffer (0x7FFF00000100), then RSP is set to 0x7FFF00000100.
        # `pop rbp` pops 8 bytes from RSP into RBP, so RSP becomes 0x7FFF00000108.
        # `ret` pops the next 8 bytes from RSP (offset 8 in our buffer) into RIP!
        
        if corrupted_rbp == buffer_addr:
            print("[+] RBP now points to our buffer.")
            print("[+] The subsequent `ret` will pop the return address from offset 8 of our buffer!")
            
            # The return address is at offset 8
            hijacked_rip = struct.unpack("<Q", buffer_content[8:16])[0]
            print(f"[+] Instruction Pointer hijacked to : {hex(hijacked_rip)}")
            
            if hijacked_rip == WIN_ADDR:
                print("\n[!] Execution redirected to win()!")
                print(f"[*] FLAG: {FLAG}")
                sys.exit(0)
            else:
                print("[-] Segmentation fault (Core dumped)")
                sys.exit(1)
        else:
            print("[-] RBP pivoted, but not to our buffer.")
            sys.exit(1)
            
    else:
        print("[-] RBP was not corrupted. Program exits normally.")
        sys.exit(0)

if __name__ == "__main__":
    main()
