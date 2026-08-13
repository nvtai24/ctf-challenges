# 26 - IntegerOverflow

## Description
A classic logic vulnerability simulating a 32-bit signed integer overflow in C. You have $100, but the flag costs $1,000,000. Can you exploit the shop's math?

## Vulnerability
When calculating `total = qty * price`, a C program using 32-bit signed integers will wrap around to a negative number if the total exceeds `2147483647` (`0x7FFFFFFF`).
Because the total cost becomes negative, checking `total <= balance` succeeds (since negative numbers are less than 100). Subtracting the negative total `balance -= total` effectively adds the amount to your balance!

## Exploit
1. Connect via TCP (`nc <ip> <port>`).
2. Choose to buy a health potion (Price: $10).
3. The max positive 32-bit integer is `2147483647`. We want `qty * 10 > 2147483647`.
4. If we buy `214748365` potions: `214748365 * 10 = 2147483650`.
5. In a 32-bit signed int, `2147483650` wraps around to `-2147483646`.
6. Enter quantity: `214748365`.
7. Cost becomes `$-2147483646`. The purchase is successful, and your balance becomes `$2147483746`.
8. Buy the flag!

**Flag:** `FCTF{1nt3g3r_0v3rfl0w_m4k3s_y0u_r1ch}`
