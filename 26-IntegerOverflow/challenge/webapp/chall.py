import os
import sys

FLAG = os.environ.get("FLAG", "FCTF{1nt3g3r_0v3rfl0w_m4k3s_y0u_r1ch}")

BANNER = r"""
  ___       _                       ___                     __ _               
 |_ _|_ __ | |_ ___  __ _  ___ _ __/ _ \__   _____ _ __  / _| | _____      __
  | || '_ \| __/ _ \/ _` |/ _ \ '__| | | \ \ / / _ \ '__| | |_| |/ _ \ \ /\ / /
  | || | | | ||  __/ (_| |  __/ |  | |_| |\ V /  __/ |  |  _| | (_) \ V  V / 
 |___|_| |_|\__\___|\__, |\___|_|   \___/  \_/ \___|_|  |_| |_|\___/ \_/\_/  
                    |___/                                                    
                           Binary Exploitation Lab
"""

def main():
    print(BANNER)
    print("Welcome to the CTF Item Shop!")
    print("Due to recent inflation, everything is expensive.")
    print("But wait! Are the cash registers using 32-bit signed integers?\n")
    sys.stdout.flush()

    balance = 100
    flag_price = 1000000

    while True:
        print("-" * 40)
        print(f"Current Balance: ${balance}")
        print("1. Buy a health potion ($10)")
        print("2. Buy a mana potion ($20)")
        print(f"3. Buy the FLAG (${flag_price})")
        print("4. Exit")
        print("-" * 40)
        sys.stdout.flush()

        try:
            choice = input("Choice> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[-] Disconnected")
            sys.exit(1)

        if choice == '1':
            price = 10
        elif choice == '2':
            price = 20
        elif choice == '3':
            price = flag_price
        elif choice == '4':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice.")
            continue
            
        if choice in ['1', '2']:
            try:
                qty_str = input("How many do you want to buy? ").strip()
                qty = int(qty_str)
            except ValueError:
                print("Invalid quantity.")
                continue
            
            if qty <= 0:
                print("Quantity must be greater than 0!")
                continue
                
            # Simulate 32-bit signed integer behavior for total cost
            # In C: int total = qty * price;
            total = qty * price
            
            # Simulate 32-bit signed wrap:
            total_32bit = total & 0xFFFFFFFF
            if total_32bit >= 0x80000000:
                total_32bit -= 0x100000000
                
            print(f"Total cost: ${total_32bit}")
            sys.stdout.flush()
            
            if total_32bit > balance:
                print("You don't have enough money!")
            else:
                balance -= total_32bit
                print("Purchase successful!")
        
        elif choice == '3':
            if balance >= flag_price:
                print("\n[+] Purchase successful!")
                print(f"[!] You bought the flag! Here it is: {FLAG}\n")
                sys.exit(0)
            else:
                print("\nYou don't have enough money for the FLAG!")

if __name__ == "__main__":
    main()
