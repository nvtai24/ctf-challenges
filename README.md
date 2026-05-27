# 🚩 Web Security CTF Challenges

A comprehensive collection of **20 web security CTF challenges** covering the OWASP Top 10 and beyond. Each challenge includes detailed solutions, exploitation guides, and mitigation strategies.

## 📁 Repository Structure

```
.
├── 02-LoginBypass/          # SQL Injection
├── 03-SecretNote/           # IDOR
├── 04-FileViewer/           # Path Traversal
├── 05-CookieMonster/        # Cookie Manipulation
├── 06-GuestBook/            # XSS
├── 07-HiddenAdmin/          # Parameter Tampering
├── 08-PriceTag/             # Price Manipulation
├── 09-RobotsSecret/         # Information Disclosure
├── 10-ForgetMe/             # Weak Password Reset
├── 11-JWTCafe/              # JWT Algorithm Confusion
├── 12-BlindSearch/          # Blind SQL Injection
├── 13-UploadShell/          # File Upload RCE
├── 14-CSRFBank/             # CSRF
├── 15-XXEReader/            # XXE Injection
├── 16-RaceCondition/        # Race Condition
├── 17-SSTINote/             # Server-Side Template Injection
├── 18-GraphAdmin/           # GraphQL IDOR
├── 19-TimingOracle/         # Timing Attack
├── 20-ChainPwn/             # Multi-Step Exploit Chain
│
├── ALL_FLAGS.txt            # Quick flag reference
├── CTF_SOLUTIONS_SUMMARY.md # Quick solutions guide
├── CTF_COMPLETE_GUIDE.md    # Comprehensive learning guide
└── PAYLOAD_CHEATSHEET.md    # Common exploitation payloads
```

## 🎯 Quick Start

### For Beginners
1. Start with **CTF_COMPLETE_GUIDE.md** for an overview
2. Follow the recommended learning path
3. Begin with easy challenges (02-09)
4. Read the `SOLUTION.md` in each challenge folder

### For Experienced Users
1. Check **ALL_FLAGS.txt** for quick reference
2. Use **PAYLOAD_CHEATSHEET.md** for common payloads
3. Jump to medium/hard challenges
4. Try to solve without reading solutions first

## 📊 Challenge Difficulty

| Difficulty | Challenges | Count |
|------------|-----------|-------|
| 🟢 Easy | 02, 03, 04, 05, 06, 07, 08, 09 | 8 |
| 🟡 Medium | 10, 11, 12, 13, 14, 15, 17, 18 | 8 |
| 🔴 Hard | 16, 19, 20 | 3 |

## 🏆 All Flags

<details>
<summary>Click to reveal all flags (spoilers!)</summary>

```
02 - FCTF{sql1_1s_0ld_but_g0ld}
03 - FCTF{1d0r_1s_ev3rywh3r3}
04 - FCTF{p4th_tr4v3rs4l_g0es_brrrr}
05 - FCTF{c00k13s_4r3_n0t_s3cr3ts}
06 - FCTF{xss_st0l3_my_c00k13}
07 - FCTF{r0l3_param_byp4ss_ez}
08 - FCTF{pr1c3_t4mp3r1ng_ch34ts}
09 - FCTF{r0b0ts_l34k_s3cr3ts}
10 - FCTF{br0k3n_p4ssw0rd_r3s3t}
11 - FCTF{jwt_n0n3_4lg_byp4ss}
12 - FCTF{bl1nd_sql1_1s_p4t13nt}
13 - FCTF{f1l3_upl04d_byp4ss_rce}
14 - FCTF{csrf_n0_t0k3n_n0_s3cur1ty}
15 - FCTF{xxe_r34ds_y0ur_f1l3s}
16 - FCTF{r4c3_c0nd1t10n_d0ubl3_sp3nd}
17 - FCTF{sst1_t3mpl4t3_1nj3ct10n}
18 - FCTF{gr4phql_1d0r_n0_4uth}
19 - FCTF{t1m1ng_4tt4ck_p4t13nc3}
20 - FCTF{ch41n_3xpl01t_m4st3r}
```

</details>

## 📚 Documentation Files

### 📖 Main Guides
- **CTF_COMPLETE_GUIDE.md** - Comprehensive guide with learning paths, tips, and resources
- **CTF_SOLUTIONS_SUMMARY.md** - Quick reference for all solutions
- **PAYLOAD_CHEATSHEET.md** - Common exploitation payloads and techniques

### 🎯 Quick References
- **ALL_FLAGS.txt** - All flags in plain text format
- **Individual SOLUTION.md** - Detailed solution in each challenge folder

## 🛠️ Tools You'll Need

### Essential
- Web Browser (Chrome/Firefox)
- curl
- Python 3

### Recommended
- Burp Suite Community
- Postman
- jwt.io

### Advanced
- SQLMap
- OWASP ZAP
- Nikto

## 🎓 What You'll Learn

### Vulnerability Classes
- ✅ SQL Injection (Classic & Blind)
- ✅ Cross-Site Scripting (XSS)
- ✅ Cross-Site Request Forgery (CSRF)
- ✅ Insecure Direct Object Reference (IDOR)
- ✅ Path Traversal
- ✅ XML External Entity (XXE)
- ✅ Server-Side Template Injection (SSTI)
- ✅ Authentication Bypass
- ✅ JWT Vulnerabilities
- ✅ File Upload Vulnerabilities
- ✅ Race Conditions
- ✅ Timing Attacks
- ✅ GraphQL Security
- ✅ Business Logic Flaws

### Skills Developed
- Web application security testing
- HTTP protocol understanding
- Browser DevTools proficiency
- Scripting and automation
- Exploit development
- Security code review
- Vulnerability mitigation

## 🎯 Recommended Learning Path

### Week 1: Fundamentals (Easy Challenges)
- Day 1-2: Information Disclosure & Client-Side (09, 05, 07)
- Day 3-4: Access Control (03, 04, 08)
- Day 5-7: Basic Injection (02, 06)

### Week 2: Intermediate (Medium Challenges)
- Day 1-2: Authentication (10, 11)
- Day 3-4: Advanced Injection (12, 15, 17)
- Day 5-6: File Upload & CSRF (13, 14)
- Day 7: API Security (18)

### Week 3: Advanced (Hard Challenges)
- Day 1-3: Race Conditions (16)
- Day 4-5: Timing Attacks (19)
- Day 6-7: Exploit Chaining (20)

## 📖 Additional Resources

### Learning Platforms
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)

### Documentation
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [HackTricks](https://book.hacktricks.xyz/)

## ⚠️ Legal Disclaimer

**IMPORTANT:** These challenges are for educational purposes only.

- ✅ Use only on systems you own or have explicit permission to test
- ❌ Never use these techniques on production systems without authorization
- ❌ Unauthorized access to computer systems is illegal
- ✅ Always follow responsible disclosure practices

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or issues
- Suggest improvements
- Add alternative solutions
- Create new challenges

## 📝 License

Educational use only. Please use responsibly.

## 🎯 Progress Tracker

Track your progress:

```
Easy Challenges:
[ ] 02 - LoginBypass
[ ] 03 - SecretNote
[ ] 04 - FileViewer
[ ] 05 - CookieMonster
[ ] 06 - GuestBook
[ ] 07 - HiddenAdmin
[ ] 08 - PriceTag
[ ] 09 - RobotsSecret

Medium Challenges:
[ ] 10 - ForgetMe
[ ] 11 - JWTCafe
[ ] 12 - BlindSearch
[ ] 13 - UploadShell
[ ] 14 - CSRFBank
[ ] 15 - XXEReader
[ ] 17 - SSTINote
[ ] 18 - GraphAdmin

Hard Challenges:
[ ] 16 - RaceCondition
[ ] 19 - TimingOracle
[ ] 20 - ChainPwn
```

## 💡 Tips for Success

1. **Read the hints** - They're designed to guide you
2. **Use DevTools** - Inspect everything
3. **Take notes** - Document your process
4. **Try variations** - One payload rarely works everywhere
5. **Be patient** - Some challenges require multiple steps
6. **Learn from failures** - Understand why something didn't work
7. **Read the code** - Understanding the vulnerability is key

## 🏅 Achievement Milestones

- 🥉 **Bronze** - Complete all Easy challenges (8/8)
- 🥈 **Silver** - Complete all Easy + Medium challenges (16/19)
- 🥇 **Gold** - Complete all challenges (19/19)
- 💎 **Platinum** - Complete all without reading solutions first

---

**Happy Hacking! 🚩**

*Remember: The goal is to learn, not just to get flags. Understand why each vulnerability exists and how to prevent it in real applications.*

---

## 📞 Support

If you have questions or need help:
1. Read the `SOLUTION.md` file in the challenge folder
2. Check the `CTF_COMPLETE_GUIDE.md` for tips
3. Review the `PAYLOAD_CHEATSHEET.md` for common techniques
4. Try different variations of your exploit

Good luck and enjoy learning! 🎓
