import os
import sys

FLAG = os.environ.get("FLAG", "FCTF{u4f_d4ngl1ng_p01nt3r_1s_b4d}")

BANNER = r"""
  _   _          _____ 
 | | | |   /\   |  ___|
 | | | |  /  \  | |__  
 | | | | / /\ \ |  __| 
 | |_| |/ ____ \| |    
  \___//_/    \_\_|    
  Binary Exploitation Lab
"""

class Note:
    def __init__(self, content=""):
        self.content = content
        
class AdminTicket:
    def __init__(self):
        self.is_admin = True
        self.secret = FLAG

def main():
    print(BANNER)
    print("Welcome to the Note Taker & Admin Ticketing system.")
    print("Can you read the admin's secret ticket?\n")
    sys.stdout.flush()
    
    # Simulate heap
    heap = {}
    next_id = 0
    
    # Pointers that we keep
    notes = {}
    admin_ticket = None
    
    while True:
        print("-" * 40)
        print("1. Create Note")
        print("2. Free Note")
        print("3. Read Note")
        print("4. Request Admin Ticket")
        print("5. Exit")
        print("-" * 40)
        sys.stdout.flush()

        try:
            choice = input("> ").strip()
        except:
            print("\n[-] Disconnected")
            sys.exit(1)

        if choice == '1':
            content = input("Note content: ").strip()
            # Allocate chunk
            chunk_id = next_id
            heap[chunk_id] = Note(content)
            # Store pointer
            notes[chunk_id] = chunk_id # stores the ID as a pointer
            print(f"[+] Note allocated at chunk ID {chunk_id}")
            next_id += 1
            
        elif choice == '2':
            nid_str = input("Note ID to free: ").strip()
            if not nid_str.isdigit():
                continue
            nid = int(nid_str)
            
            # The vulnerability: Freeing the chunk but keeping the pointer in `notes`
            if nid in heap:
                del heap[nid]
                print(f"[+] Chunk {nid} freed.")
                print("[!] Oops, forgot to clear the pointer in the notes list! (Dangling pointer created)")
            else:
                print("[-] Chunk not found or already freed.")
                
        elif choice == '3':
            nid_str = input("Note ID to read: ").strip()
            if not nid_str.isdigit():
                continue
            nid = int(nid_str)
            
            if nid in notes: # Checking the dangling pointer!
                chunk_id = notes[nid]
                if chunk_id in heap:
                    # In C, it would just cast the raw memory back to Note*
                    # We simulate this by just printing whatever object is there!
                    obj = heap[chunk_id]
                    if isinstance(obj, Note):
                        print(f"Content: {obj.content}")
                    elif isinstance(obj, AdminTicket):
                        print("Warning: Type confusion! Reading AdminTicket as a Note struct...")
                        print(f"Content (is_admin): {obj.is_admin}")
                        print(f"Content (secret): {obj.secret}")
                else:
                    print("[-] Dereferencing unmapped memory (Segfault)")
            else:
                print("[-] Invalid note ID")
                
        elif choice == '4':
            # Allocating an AdminTicket
            if not admin_ticket:
                # Find the lowest available chunk ID in heap (simulating malloc reusing freed chunks)
                available = set(range(next_id)) - set(heap.keys())
                if available:
                    chunk_id = min(available)
                    print(f"[+] malloc() is reusing freed chunk {chunk_id} for the Admin Ticket!")
                else:
                    chunk_id = next_id
                    next_id += 1
                
                heap[chunk_id] = AdminTicket()
                admin_ticket = chunk_id
                print(f"[+] Admin Ticket allocated at chunk ID {chunk_id}")
            else:
                print("[-] Admin Ticket already exists!")
                
        elif choice == '5':
            print("Goodbye")
            sys.exit(0)
            
if __name__ == "__main__":
    main()
