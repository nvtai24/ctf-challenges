# 27 - UseAfterFree

## Description
A classic heap Use-After-Free (UAF) challenge. The program lets you allocate notes, free them, and allocate an Admin Ticket. 

## Vulnerability
When a note is freed (Option 2), its corresponding pointer in the `notes` list is NOT cleared. This leaves a dangling pointer.
When a new object (like the `AdminTicket`) is allocated, `malloc` reuses the most recently freed memory chunk to save space. 
Since we still have a pointer to this memory chunk (our freed note), we can read it to access the `AdminTicket`'s properties!

## Exploit
1. Connect via TCP (`nc <ip> <port>`).
2. Create a Note (`1`) with any content. It will be allocated at chunk `0`.
3. Free Note `0` (`2`). The memory is returned to the heap, but pointer `0` still exists.
4. Request Admin Ticket (`4`). It will reuse the freed chunk `0`.
5. Read Note `0` (`3`). The program will interpret the memory at chunk `0` (which is now an `AdminTicket`) as a Note, causing a Type Confusion that leaks the flag!

**Flag:** `FCTF{u4f_d4ngl1ng_p01nt3r_1s_b4d}`
