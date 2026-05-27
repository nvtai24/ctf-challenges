# Complete CTF Challenge Guide

## 🎯 Overview

This repository contains **20 web security CTF challenges** covering the most common vulnerabilities found in modern web applications. Each challenge is designed to teach a specific vulnerability class with hands-on exploitation.

## 📊 Challenge Statistics

- **Total Challenges:** 20
- **Easy:** 8 challenges (02-09)
- **Medium:** 8 challenges (10-15, 17-18)
- **Hard:** 4 challenges (16, 19, 20)

## 🗂️ Complete Challenge List

### Easy Challenges (Beginner Friendly)

| # | Name | Vulnerability | Flag |
|---|------|---------------|------|
| 02 | LoginBypass | SQL Injection | `FCTF{sql1_1s_0ld_but_g0ld}` |
| 03 | SecretNote | IDOR | `FCTF{1d0r_1s_ev3rywh3r3}` |
| 04 | FileViewer | Path Traversal | `FCTF{p4th_tr4v3rs4l_g0es_brrrr}` |
| 05 | CookieMonster | Cookie Manipulation | `FCTF{c00k13s_4r3_n0t_s3cr3ts}` |
| 06 | GuestBook | XSS (Reflected) | `FCTF{xss_st0l3_my_c00k13}` |
| 07 | HiddenAdmin | Parameter Tampering | `FCTF{r0l3_param_byp4ss_ez}` |
| 08 | PriceTag | Price Manipulation | `FCTF{pr1c3_t4mp3r1ng_ch34ts}` |
| 09 | RobotsSecret | Information Disclosure | `FCTF{r0b0ts_l34k_s3cr3ts}` |

### Medium Challenges (Intermediate)

| # | Name | Vulnerability | Flag |
|---|------|---------------|------|
| 10 | ForgetMe | Weak Password Reset | `FCTF{br0k3n_p4ssw0rd_r3s3t}` |
| 11 | JWTCafe | JWT Algorithm Confusion | `FCTF{jwt_n0n3_4lg_byp4ss}` |
| 12 | BlindSearch | Blind SQL Injection | `FCTF{bl1nd_sql1_1s_p4t13nt}` |
| 13 | UploadShell | File Upload RCE | `FCTF{f1l3_upl04d_byp4ss_rce}` |
| 14 | CSRFBank | CSRF | `FCTF{csrf_n0_t0k3n_n0_s3cur1ty}` |
| 15 | XXEReader | XXE Injection | `FCTF{xxe_r34ds_y0ur_f1l3s}` |
| 17 | SSTINote | Server-Side Template Injection | `FCTF{sst1_t3mpl4t3_1nj3ct10n}` |
| 18 | GraphAdmin | GraphQL IDOR | `FCTF{gr4phql_1d0r_n0_4uth}` |

### Hard Challenges (Advanced)

| # | Name | Vulnerability | Flag |
|---|------|---------------|------|
| 16 | RaceCondition | Race Condition | `FCTF{r4c3_c0nd1t10n_d0ubl3_sp3nd}` |
| 19 | TimingOracle | Timing Attack | `FCTF{t1m1ng_4tt4ck_p4t13nc3}` |
| 20 | ChainPwn | Multi-Step Exploit Chain | `FCTF{ch41n_3xpl01t_m4st3r}` |

## 🎓 Learning Path

### Path 1: Web Basics (Start Here)
1. **09 - RobotsSecret** - Information disclosure
2. **05 - CookieMonster** - Client-side security
3. **07 - HiddenAdmin** - Parameter tampering
4. **08 - PriceTag** - Business logic flaws

### Path 2: Injection Attacks
1. **02 - LoginBypass** - SQL Injection basics
2. **12 - BlindSearch** - Blind SQL Injection
3. **06 - GuestBook** - XSS
4. **15 - XXEReader** - XXE
5. **17 - SSTINote** - SSTI

### Path 3: Access Control
1. **03 - SecretNote** - IDOR
2. **04 - FileViewer** - Path Traversal
3. **18 - GraphAdmin** - GraphQL IDOR

### Path 4: Authentication & Sessions
1. **10 - ForgetMe** - Password reset flaws
2. **11 - JWTCafe** - JWT vulnerabilities
3. **14 - CSRFBank** - CSRF attacks

### Path 5: Advanced Topics
1. **13 - UploadShell** - File upload RCE
2. **16 - RaceCondition** - Concurrency issues
3. **19 - TimingOracle** - Side-channel attacks
4. **20 - ChainPwn** - Exploit chaining

## 🛠️ Required Tools

### Essential
- **Web Browser** (Chrome/Firefox with DevTools)
- **curl** - Command-line HTTP client
- **Python 3** - For automation scripts

### Recommended
- **Burp Suite Community** - HTTP proxy and testing
- **Postman** - API testing
- **jwt.io** - JWT decoder
- **CyberChef** - Data encoding/decoding

### Advanced
- **SQLMap** - Automated SQL injection
- **Nikto** - Web scanner
- **OWASP ZAP** - Security testing proxy

## 📚 Vulnerability Categories

### OWASP Top 10 Coverage

#### A01: Broken Access Control
- 03 - SecretNote (IDOR)
- 07 - HiddenAdmin (Parameter Tampering)
- 18 - GraphAdmin (GraphQL IDOR)

#### A02: Cryptographic Failures
- 05 - CookieMonster (Insecure Storage)
- 10 - ForgetMe (Weak Tokens)
- 11 - JWTCafe (Weak JWT)

#### A03: Injection
- 02 - LoginBypass (SQL Injection)
- 06 - GuestBook (XSS)
- 12 - BlindSearch (Blind SQLi)
- 15 - XXEReader (XXE)
- 17 - SSTINote (SSTI)

#### A04: Insecure Design
- 08 - PriceTag (Logic Flaw)
- 16 - RaceCondition (TOCTOU)
- 19 - TimingOracle (Side-Channel)

#### A05: Security Misconfiguration
- 04 - FileViewer (Path Traversal)
- 09 - RobotsSecret (Info Disclosure)

#### A07: Identification and Authentication Failures
- 10 - ForgetMe (Password Reset)
- 11 - JWTCafe (JWT Bypass)

#### A08: Software and Data Integrity Failures
- 13 - UploadShell (File Upload)

#### A10: Server-Side Request Forgery
- 14 - CSRFBank (CSRF)

## 🚀 Quick Start Guide

### For Each Challenge:

1. **Read the Challenge**
   - Navigate to challenge directory
   - Read `SOLUTION.md` for hints (or full solution)

2. **Understand the Vulnerability**
   - Review the vulnerable code
   - Understand why it's exploitable

3. **Exploit It**
   - Follow the exploitation steps
   - Try to find the flag yourself first

4. **Learn the Mitigation**
   - Study the secure code examples
   - Understand how to prevent the vulnerability

## 💡 Tips for Success

### General Tips
- **Read the hints** - They're there to help
- **Use DevTools** - Inspect requests, cookies, and responses
- **Take notes** - Document your findings
- **Try variations** - One payload might not work everywhere
- **Be patient** - Some challenges require multiple steps

### For SQL Injection
- Start with simple payloads: `' OR '1'='1`
- Use `--` or `#` to comment out the rest
- Try UNION attacks for data extraction

### For XSS
- Test with simple payloads: `<script>alert(1)</script>`
- Try different contexts: HTML, attributes, JavaScript
- Use `<img src=x onerror=...>` if `<script>` is blocked

### For IDOR
- Look for numeric IDs in URLs
- Try incrementing/decrementing IDs
- Check if authorization is enforced

### For JWT
- Decode the token at jwt.io
- Try changing the algorithm to "none"
- Modify the payload and re-encode

## 📖 Additional Resources

### Learning Platforms
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)
- [PentesterLab](https://pentesterlab.com/)

### Documentation
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [HackTricks](https://book.hacktricks.xyz/)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)

### Books
- "The Web Application Hacker's Handbook" by Dafydd Stuttard
- "Real-World Bug Hunting" by Peter Yaworski
- "Web Security Testing Cookbook" by Paco Hope

## 🏆 Challenge Completion Checklist

Track your progress:

- [ ] 02 - LoginBypass
- [ ] 03 - SecretNote
- [ ] 04 - FileViewer
- [ ] 05 - CookieMonster
- [ ] 06 - GuestBook
- [ ] 07 - HiddenAdmin
- [ ] 08 - PriceTag
- [ ] 09 - RobotsSecret
- [ ] 10 - ForgetMe
- [ ] 11 - JWTCafe
- [ ] 12 - BlindSearch
- [ ] 13 - UploadShell
- [ ] 14 - CSRFBank
- [ ] 15 - XXEReader
- [ ] 16 - RaceCondition
- [ ] 17 - SSTINote
- [ ] 18 - GraphAdmin
- [ ] 19 - TimingOracle
- [ ] 20 - ChainPwn

## 🎯 Skill Development

### After Completing Easy Challenges
You should understand:
- Basic web vulnerabilities
- HTTP requests and responses
- Browser DevTools
- Simple exploitation techniques

### After Completing Medium Challenges
You should understand:
- Advanced injection techniques
- Authentication bypass methods
- File upload vulnerabilities
- API security issues

### After Completing Hard Challenges
You should understand:
- Race conditions and timing attacks
- Multi-step exploitation
- Complex vulnerability chains
- Advanced attack techniques

## ⚠️ Legal Disclaimer

These challenges are for **educational purposes only**. 

- Only test on systems you own or have explicit permission to test
- Never use these techniques on production systems without authorization
- Unauthorized access to computer systems is illegal
- Always follow responsible disclosure practices

## 🤝 Contributing

Found an issue or want to improve a challenge?
- Report bugs
- Suggest improvements
- Add alternative solutions
- Create new challenges

## 📝 License

Educational use only. Please use responsibly.

---

**Happy Hacking! 🚩**

Remember: The goal is to learn, not just to get flags. Understand *why* each vulnerability exists and *how* to prevent it in real applications.
