# CTF Challenge Templates

A repository of **CTF challenge templates** (Capture The Flag) — use them as starting points when authoring challenges, deploying a platform, or practicing. Templates will be added over time, organized by category.

## Table of Contents

- [Purpose](#purpose)
- [Repository structure (planned)](#repository-structure-planned)
- [Common platform categories](#common-platform-categories)
- [CTF challenge types by skill](#ctf-challenge-types-by-skill)
  - [1. Web Exploitation](#1-web-exploitation-web)
  - [2. Binary Exploitation](#2-binary-exploitation-pwn--pwning)
  - [3. Reverse Engineering](#3-reverse-engineering-rev)
  - [4. Cryptography](#4-cryptography-crypto)
  - [5. Forensics](#5-forensics)
  - [6. Miscellaneous](#6-miscellaneous-misc)
  - [7. OSINT](#7-osint-open-source-intelligence)
  - [8. Steganography](#8-steganography)
  - [9. Mobile Security](#9-mobile-security)
  - [10. Cloud / Container / Infrastructure](#10-cloud--container--infrastructure)
  - [11. Network](#11-network)
  - [12. Hardware / IoT](#12-hardware--iot)
  - [13. AI / ML Security](#13-ai--ml-security)
- [Challenge metadata guidelines](#challenge-metadata-guidelines)

---

## Purpose

- Catalog **common CTF challenge types**, grouped by security skill or technique.
- Serve as a **reference** when creating new templates in this repo.
- Not a full challenge list — only a taxonomy of techniques and topics you will see often.

## Repository structure (planned)

```
ctf-challenges/
├── web/
├── pwn/
├── rev/
├── crypto/
├── forensics/
├── misc/
├── osint/
├── stego/
├── mobile/
├── cloud/
├── network/
├── hardware/
└── ai/
```

Each folder will hold challenge templates (description, deploy files, sample writeups, etc.) as they are added.

## Common platform categories

Many modern CTF platforms use these **core categories**:

| Category   | Brief description                    |
| ---------- | ------------------------------------ |
| Web        | Web application exploitation         |
| Pwn        | Binary exploitation                  |
| Rev        | Reverse engineering                  |
| Crypto     | Cryptography                         |
| Forensics  | Digital forensics (logs, memory, disk) |
| Misc       | Catch-all / mixed topics             |
| OSINT      | Open-source intelligence gathering   |
| Cloud      | Cloud, containers, infrastructure    |
| Mobile     | Android / iOS                        |
| Hardware   | IoT, firmware, hardware              |
| AI         | ML / LLM security (emerging)       |

---

## CTF challenge types by skill

### 1. Web Exploitation (Web)

| Technique | Notes |
| --------- | ----- |
| SQL Injection (SQLi) | Injection via database input |
| Cross-Site Scripting (XSS) | Reflected / Stored / DOM |
| Server-Side Request Forgery (SSRF) | Server fetches attacker-controlled URLs |
| Local / Remote File Inclusion (LFI / RFI) | Include files from server or remote host |
| Command Injection | OS command execution via input |
| Authentication Bypass | Circumvent login / auth checks |
| JWT Attack | Tampering, secret brute force, alg confusion |
| CSRF | Cross-Site Request Forgery |
| Deserialization | Unsafe object deserialization |
| Prototype Pollution | JavaScript object prototype abuse |
| Race Condition | Time-of-check vs time-of-use bugs |
| File Upload Vulnerability | Web shell upload / filter bypass |
| Path Traversal | Read files outside allowed directories |
| SSTI | Server-Side Template Injection |
| Business Logic Bug | Application logic flaws, not classic CVEs |

### 2. Binary Exploitation (Pwn / Pwning)

- Buffer Overflow / Stack Overflow
- Heap Exploitation
- Format String Vulnerability
- Return Oriented Programming (ROP)
- Shellcode Injection
- Use After Free (UAF)
- Integer Overflow
- Race Condition
- Bypassing mitigations: **NX**, **PIE**, **ASLR**, **Canary**

### 3. Reverse Engineering (Rev)

- Analyzing `.exe`, ELF, APK binaries
- Obfuscation, anti-debugging
- Crackme, keygenme
- Bytecode analysis
- Introductory malware analysis
- Decompile / disassemble
- Dynamic analysis (debugger, tracing)

### 4. Cryptography (Crypto)

- Caesar / Vigenère cipher
- RSA attacks (small exponent, common modulus, etc.)
- AES mode weaknesses (ECB, padding issues, etc.)
- XOR cipher
- Padding Oracle
- Hash collision
- PRNG predictability, LCG attack
- Lattice attack
- Timing attack

### 5. Forensics

- PCAP analysis (Wireshark)
- Memory dump analysis
- Disk image analysis
- Metadata extraction
- Steganography (within forensics)
- File carving
- Log analysis
- USB artifacts, registry analysis
- Hidden data recovery

### 6. Miscellaneous (Misc)

- QR codes, encoding / decoding
- CAPTCHA bypass
- Light OSINT (sometimes its own category)
- Math puzzles, programming challenges
- Bash / Python scripting
- Network traffic, automation

### 7. OSINT (Open Source Intelligence)

- Finding public information (names, locations, timestamps)
- Social media investigation
- Image metadata (EXIF)
- Domain enumeration, DNS recon
- Git leaks, Google dorking
- Archive.org and other public archives

### 8. Steganography

Hiding data in:

- Images, audio, video, PDFs

Common techniques:

- LSB extraction
- Image layer analysis
- Audio spectrograms

### 9. Mobile Security

- Android APK reversing
- Frida bypass (runtime hooking)
- Root detection bypass
- SSL pinning bypass
- iOS app analysis

### 10. Cloud / Container / Infrastructure

- Kubernetes misconfiguration
- Docker escape
- IAM misconfiguration
- Secret leaks (env, config, vault)
- CI/CD exploitation
- Cloud bucket exposure (S3, GCS, etc.)

### 11. Network

- Packet analysis
- TCP/IP attacks
- DNS tunneling
- ARP spoofing, MITM
- Protocol reverse engineering

### 12. Hardware / IoT

- UART, JTAG
- Firmware extraction
- RFID / NFC
- Side-channel attacks

### 13. AI / ML Security

> A newer category, increasingly common at CTF events.

- Prompt injection
- Model extraction
- LLM jailbreak
- Data poisoning
- Adversarial input

---

## Challenge metadata guidelines

When authoring templates or publishing to a platform, include:

| Field | Examples |
| ----- | -------- |
| **Difficulty** | `Easy` · `Medium` · `Hard` · `Insane` |
| **Tags** | `xss`, `jwt`, `heap`, `rsa`, `k8s`, `docker`, `lsb`, … |
| **Category** | One of the core categories in the table above |

Tags help filtering and hint at solution paths; difficulty helps balance the scoreboard.

---

*This repo is in early setup — per-topic templates will be added over time.*
