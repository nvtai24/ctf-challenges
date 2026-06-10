import os
import sys
import random
import struct

FLAG = os.environ.get("FLAG", "CTF{placeholder}")

BANNER = r"""
  _____                          _     ____  _        _
 |  ___|__  _ __ _ __ ___   __ _| |_  / ___|| |_ _ __(_)_ __   __ _
 | |_ / _ \| '__| '_ ` _ \ / _` | __| \___ \| __| '__| | '_ \ / _` |
 |  _| (_) | |  | | | | | | (_| | |_   ___) | |_| |  | | | | | (_| |
 |_|  \___/|_|  |_| |_| |_|\__,_|\__| |____/ \__|_|  |_|_| |_|\__, |
                                                                 |___/
                          Binary Exploitation Lab
"""

WIN_ADDR = 0x401337


def simulate_printf(fmt: str, stack: list) -> str:
    """
    Simulate C's printf(user_input) with format string vulnerability.
    Supports %p, %x, %d and positional %N$p / %N$x / %N$d (1-indexed).
    Stack indices are 0-based internally.
    """
    output_parts = []
    i = 0
    seq_idx = 0  # sequential argument counter

    while i < len(fmt):
        if fmt[i] != "%" or i + 1 >= len(fmt):
            output_parts.append(fmt[i])
            i += 1
            continue

        i += 1  # skip '%'
        spec_start = i

        # Check for positional argument: digits followed by '$' and a specifier
        j = i
        while j < len(fmt) and fmt[j].isdigit():
            j += 1

        if j > i and j < len(fmt) and fmt[j] == "$" and j + 1 < len(fmt) and fmt[j + 1] in "pxd":
            pos = int(fmt[i:j]) - 1  # convert 1-indexed to 0-indexed
            spec = fmt[j + 1]
            i = j + 2
            val = stack[pos] if 0 <= pos < len(stack) else 0
            if spec in ("p", "x"):
                output_parts.append(f"0x{val:016x}")
            else:
                output_parts.append(str(val))
            continue

        # Sequential specifier
        if fmt[i] in "pxd":
            spec = fmt[i]
            i += 1
            val = stack[seq_idx] if seq_idx < len(stack) else 0
            seq_idx += 1
            if spec in ("p", "x"):
                output_parts.append(f"0x{val:016x}")
            else:
                output_parts.append(str(val))
        else:
            # Not a recognised specifier — emit literally
            output_parts.append(f"%{fmt[spec_start]}")
            i = spec_start + 1

    return "".join(output_parts)


def main():
    print(BANNER)
    print("A vulnerable C program is running.")
    print("It calls printf(user_input) directly — classic format string bug.\n")

    # Stack canary: random 8-byte value, low byte always 0x00 (null-byte trick)
    canary = random.randint(0x0100000000000000, 0x7EFFFFFFFFFFFFFF) & ~0xFF

    # Simulated stack visible through format string (8 qwords):
    #
    #  index | content
    # -------+-----------------------------------------
    #   0    | local var A
    #   1    | local var B
    #   2    | local var C
    #   3    | stack canary   <- you need to leak this
    #   4    | saved RBP
    #   5    | return address
    #   6    | arg 1 (unused)
    #   7    | arg 2 (unused)
    #
    stack = [
        0x4141414141414141,
        0x00007FFF5FBFF260,
        0x0000000000000000,
        canary,             # index 3 → positional arg %4$p
        0x00007FFF5FBFF120,
        0x000000000040128A,
        0x0000000000000001,
        0x0000000000000000,
    ]

    print(f"  win() lives at: {hex(WIN_ADDR)}")
    print( "  The stack has 8 qwords readable via format string args.\n")
    print("━" * 60)
    print("  STAGE 1 — Leak the stack canary via format string")
    print("━" * 60)
    print("  The vulnerable call: printf(user_input)")
    print("  Use %N$p to read the N-th stack argument (1-indexed).\n")
    sys.stdout.flush()

    try:
        fmt = input("[fmt]> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[-] Disconnected")
        sys.exit(1)

    if len(fmt) > 128:
        print("[-] Input too long (max 128 chars)")
        sys.exit(1)

    result = simulate_printf(fmt, stack)
    print(f"[printf]: {result}\n")
    sys.stdout.flush()

    print("━" * 60)
    print("  STAGE 2 — Overflow the buffer with correct canary")
    print("━" * 60)
    print("  Stack layout at vulnerable strcpy():")
    print()
    print("   offset 0x00 : [ buffer          32 bytes ]")
    print("   offset 0x20 : [ stack canary     8 bytes ]  <- must match!")
    print("   offset 0x28 : [ saved RBP        8 bytes ]  <- anything")
    print("   offset 0x30 : [ return address   8 bytes ]  <- set to win()")
    print()
    print(f"  Target: return address = {hex(WIN_ADDR)}")
    print("  Payload format: hex-encoded bytes\n")
    sys.stdout.flush()

    try:
        raw = input("[payload]> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[-] Disconnected")
        sys.exit(1)

    try:
        payload = bytes.fromhex(raw)
    except ValueError:
        print("[-] Invalid hex")
        sys.exit(1)

    if len(payload) < 56:
        print(f"[-] Too short ({len(payload)} bytes) — didn't reach return address (need 56)")
        sys.exit(0)

    submitted_canary = struct.unpack("<Q", payload[32:40].ljust(8, b"\x00"))[0]
    submitted_ret    = struct.unpack("<Q", payload[48:56].ljust(8, b"\x00"))[0]

    print()
    if submitted_canary != canary:
        print("*** stack smashing detected ***")
        print(f"    canary expected : {hex(canary)}")
        print(f"    canary got      : {hex(submitted_canary)}")
        print("[-] Aborted.")
        sys.exit(0)

    print(f"[+] Canary OK       : {hex(canary)}")
    print(f"[i] Return address  : {hex(submitted_ret)}")
    sys.stdout.flush()

    if submitted_ret == WIN_ADDR:
        print()
        print("[!] Jumping to win()!")
        print(f"[*] FLAG: {FLAG}")
    else:
        print("[-] Segmentation fault (core dumped)")
        print(f"    Expected : {hex(WIN_ADDR)}")
        print(f"    Got      : {hex(submitted_ret)}")


if __name__ == "__main__":
    main()
