import os
import sys
import struct

FLAG = os.environ.get("FLAG", "CTF{placeholder}")

BANNER = r"""
  ____  _             _     ____  __  __    _    ____  _   _
 / ___|| |_ __ _  ___| | __/ ___||  \/  |  / \  / ___|| | | |
 \___ \| __/ _` |/ __| |/ /\___ \| |\/| | / _ \ \___ \| |_| |
  ___) | || (_| | (__|   <  ___) | |  | |/ ___ \ ___) |  _  |
 |____/ \__\__,_|\___|_|\_\|____/|_|  |_/_/   \_\____/|_| |_|

                   Binary Exploitation Lab
"""

# Simulated addresses
BUFFER_ADDR = 0x7FFF5FBFF0E0
WIN_ADDR    = 0xDEADBEEFCAFE


def win():
    print()
    print("[!] RIP controlled — jumping to win()!")
    print(f"[*] FLAG: {FLAG}")
    sys.stdout.flush()
    sys.exit(0)


def vuln():
    # Stack layout (x86-64 calling convention simulation):
    #   [0x00 - 0x1F]  buffer      (32 bytes)
    #   [0x20 - 0x27]  saved RBP   (8 bytes)
    #   [0x28 - 0x2F]  return addr (8 bytes)  <- overwrite this with WIN_ADDR
    #
    # Total offset to ret addr: 40 bytes (32 buf + 8 saved_rbp)

    print(f"[i] &buffer  = {hex(BUFFER_ADDR)}")
    print(f"[i] &win()   = {hex(WIN_ADDR)}")
    print()
    print("    Stack layout:")
    print(f"    {hex(BUFFER_ADDR)}  +-----------------------+")
    print(f"                   |   buffer  (32 bytes)  |")
    print(f"    {hex(BUFFER_ADDR+0x20)}  +-----------------------+")
    print(f"                   |   saved RBP (8 bytes) |")
    print(f"    {hex(BUFFER_ADDR+0x28)}  +-----------------------+")
    print(f"                   |  return addr (8 bytes)|  <-- overwrite me!")
    print(f"    {hex(BUFFER_ADDR+0x30)}  +-----------------------+")
    print()
    print("Enter payload as hex (e.g. 41414141...deadbeefcafe):")
    sys.stdout.flush()

    try:
        raw = input("> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[-] Connection closed")
        sys.exit(1)

    try:
        data = bytes.fromhex(raw)
    except ValueError:
        print("[-] Invalid hex input — only [0-9a-fA-F] characters please")
        return

    if len(data) < 48:
        print(f"[i] Wrote {len(data)} bytes — didn't reach return address (need at least 48)")
        print("[-] Program exits normally")
        return

    # Extract the overwritten return address (little-endian, 8 bytes at offset 40)
    ret_bytes = data[40:48]
    ret_addr = struct.unpack("<Q", ret_bytes)[0]
    print(f"[i] return address overwritten: {hex(ret_addr)}")
    sys.stdout.flush()

    if ret_addr == WIN_ADDR:
        win()
    else:
        print("[-] Segmentation fault (core dumped)")
        print(f"    Expected: {hex(WIN_ADDR)}")
        print(f"    Got:      {hex(ret_addr)}")


def main():
    print(BANNER)
    print("A classic stack-based buffer overflow challenge.")
    print("Overflow the buffer and redirect execution to win()!\n")
    sys.stdout.flush()
    vuln()


if __name__ == "__main__":
    main()
