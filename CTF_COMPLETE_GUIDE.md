# Cẩm nang thử thách CTF toàn tập

## 🎯 Tổng quan

Kho lưu trữ này chứa **20 thử thách CTF bảo mật Web và Pwn** bao quát hầu hết các nhóm lỗ hổng phổ biến nhất được tìm thấy trong các hệ thống hiện đại. Mỗi thử thách được thiết kế có chủ đích để dạy bạn một kỹ thuật khai thác thực chiến.

## 📊 Thống kê Thử thách

- **Tổng số bài:** 20
- **Dễ (Easy):** 8 bài (02-09)
- **Trung bình (Medium):** 8 bài (10-15, 17-18)
- **Khó (Hard):** 4 bài (16, 19, 20)

## 🗂️ Danh sách Thử thách đầy đủ

### Mức độ Dễ (Thân thiện với người mới)

| # | Tên | Loại lỗ hổng | Flag |
|---|------|---------------|------|
| 02 | LoginBypass | SQL Injection | `FCTF{sql1_1s_0ld_but_g0ld}` |
| 03 | SecretNote | IDOR (Lỗi kiểm soát truy cập) | `FCTF{1d0r_1s_ev3rywh3r3}` |
| 04 | FileViewer | Path Traversal (Duyệt thư mục) | `FCTF{p4th_tr4v3rs4l_g0es_brrrr}` |
| 05 | CookieMonster | Thao túng Cookie | `FCTF{c00k13s_4r3_n0t_s3cr3ts}` |
| 06 | GuestBook | XSS (Reflected) | `FCTF{xss_st0l3_my_c00k13}` |
| 07 | HiddenAdmin | Parameter Tampering (Giả mạo tham số) | `FCTF{r0l3_param_byp4ss_ez}` |
| 08 | PriceTag | Thao túng giá (Lỗi logic) | `FCTF{pr1c3_t4mp3r1ng_ch34ts}` |
| 09 | RobotsSecret | Lộ lọt thông tin (Info Disclosure) | `FCTF{r0b0ts_l34k_s3cr3ts}` |

### Mức độ Trung bình (Nâng cao kỹ năng)

| # | Tên | Loại lỗ hổng | Flag |
|---|------|---------------|------|
| 10 | ForgetMe | Reset mật khẩu lỏng lẻo | `FCTF{br0k3n_p4ssw0rd_r3s3t}` |
| 11 | JWTCafe | Lỗ hổng JWT (Thuật toán None) | `FCTF{jwt_n0n3_4lg_byp4ss}` |
| 12 | BlindSearch | Blind SQL Injection | `FCTF{bl1nd_sql1_1s_p4t13nt}` |
| 13 | UploadShell | Lỗ hổng Upload File (RCE) | `FCTF{f1l3_upl04d_byp4ss_rce}` |
| 14 | CSRFBank | CSRF | `FCTF{csrf_n0_t0k3n_n0_s3cur1ty}` |
| 15 | XXEReader | XXE Injection | `FCTF{xxe_r34ds_y0ur_f1l3s}` |
| 17 | SSTINote | Server-Side Template Injection (SSTI) | `FCTF{sst1_t3mpl4t3_1nj3ct10n}` |
| 18 | GraphAdmin | GraphQL IDOR | `FCTF{gr4phql_1d0r_n0_4uth}` |

### Mức độ Khó (Thử thách chuyên gia)

| # | Tên | Loại lỗ hổng | Flag |
|---|------|---------------|------|
| 16 | RaceCondition | Lỗ hổng tương tranh (Race Condition) | `FCTF{r4c3_c0nd1t10n_d0ubl3_sp3nd}` |
| 19 | TimingOracle | Timing Attack (Kênh kề) | `FCTF{t1m1ng_4tt4ck_p4t13nc3}` |
| 20 | ChainPwn | Exploit Chain (Chuỗi khai thác đa bước) | `FCTF{ch41n_3xpl01t_m4st3r}` |

## 🎓 Lộ trình học tập khuyến nghị

### Chặng 1: Nền tảng Web Cơ bản
1. **09 - RobotsSecret** - Kỹ thuật OSINT & Info Disclosure
2. **05 - CookieMonster** - Hiểu về bảo mật Client-side
3. **07 - HiddenAdmin** - Thay đổi dữ liệu truyền đi
4. **08 - PriceTag** - Logic nghiệp vụ (Business Logic)

### Chặng 2: Nghệ thuật Injection
1. **02 - LoginBypass** - Căn bản về SQLi
2. **12 - BlindSearch** - Rút trích dữ liệu bằng Blind SQLi
3. **06 - GuestBook** - Khởi động với XSS
4. **15 - XXEReader** - Đọc file hệ thống bằng XXE
5. **17 - SSTINote** - Leo thang lên RCE với SSTI

### Chặng 3: Phân quyền & Kiểm soát truy cập
1. **03 - SecretNote** - Lỗi IDOR
2. **04 - FileViewer** - Leo cây thư mục (Path Traversal)
3. **18 - GraphAdmin** - Khai thác IDOR qua API GraphQL

### Chặng 4: Định danh & Quản lý Phiên
1. **10 - ForgetMe** - Bypass chức năng Quên mật khẩu
2. **11 - JWTCafe** - Bẻ khóa JWT
3. **14 - CSRFBank** - Cướp phiên người dùng bằng CSRF

### Chặng 5: Đỉnh cao Khai thác
1. **13 - UploadShell** - Chiếm quyền điều khiển máy chủ (Web Shell)
2. **16 - RaceCondition** - Lợi dụng độ trễ của cơ sở dữ liệu
3. **19 - TimingOracle** - Đo thời gian để đoán mật khẩu
4. **20 - ChainPwn** - Liên kết các lỗ hổng thành chuỗi Exploit

## 🛠️ Công cụ Hành nghề

### Bắt buộc phải có
- **Trình duyệt Web** (Chrome/Firefox sử dụng thành thạo DevTools F12)
- **cURL** - Tiện ích gửi HTTP Request qua command line
- **Python 3** - Để viết Script tự động hóa

### Rất nên dùng
- **Burp Suite Community** - Proxy bắt gói tin siêu mạnh mẽ
- **Postman** - Công cụ test API
- **jwt.io** - Giải mã/Debug token JWT
- **CyberChef** - Con dao Thụy Sĩ để Decode/Encode mọi thứ

### Nâng cao
- **SQLMap** - Tự động dò quét SQL Injection
- **OWASP ZAP** - Trình quét bảo mật Web mã nguồn mở

## 📚 Phân loại lỗ hổng theo chuẩn OWASP Top 10

#### A01: Broken Access Control (Kiểm soát truy cập lỗi)
- 03 - SecretNote (IDOR)
- 07 - HiddenAdmin (Parameter Tampering)
- 18 - GraphAdmin (GraphQL IDOR)

#### A02: Cryptographic Failures (Lỗi mật mã)
- 05 - CookieMonster (Lưu trữ plaintext)
- 10 - ForgetMe (Token dễ đoán)
- 11 - JWTCafe (Xác thực JWT kém)

#### A03: Injection (Lỗ hổng Tiêm chích)
- 02 - LoginBypass (SQLi)
- 06 - GuestBook (XSS)
- 12 - BlindSearch (Blind SQLi)
- 15 - XXEReader (XXE)
- 17 - SSTINote (SSTI)

#### A04: Insecure Design (Thiết kế thiếu an toàn)
- 08 - PriceTag (Lỗi Logic)
- 16 - RaceCondition (TOCTOU)
- 19 - TimingOracle (Lỗ hổng Side-Channel)

#### A05: Security Misconfiguration (Cấu hình sai)
- 04 - FileViewer (Path Traversal)
- 09 - RobotsSecret (Lộ thư mục nhạy cảm)

#### A07: Identification and Authentication Failures (Xác thực kém)
- 10 - ForgetMe (Lỗi cấp lại Pass)
- 11 - JWTCafe (Bypass token)

#### A08: Software and Data Integrity Failures (Lỗi toàn vẹn dữ liệu)
- 13 - UploadShell (Không kiểm duyệt file tải lên)

#### A10: Server-Side Request Forgery (SSRF)
- 14 - CSRFBank (Lỗ hổng CSRF)

## 🚀 Hướng dẫn bắt đầu

### Trình tự tiếp cận mỗi bài:
1. **Đọc kỹ đề bài:** Vào thư mục của thử thách. Đọc file `SOLUTION.md` để lấy gợi ý.
2. **Nghiên cứu nguyên nhân:** Xem mã nguồn bị lỗi, phân tích lý do tại sao nó có thể bị hack.
3. **Xắn tay áo lên:** Làm theo các bước Exploit. Cố gắng tự tìm ra Flag mà không copy paste.
4. **Học cách phòng ngự:** Nghiên cứu phần "Mitigation" (Biện pháp phòng ngừa) để biết cách lập trình an toàn.

## 💡 Bí kíp bỏ túi
- **Hãy đọc kỹ các gợi ý:** Chúng ở đó để cứu bạn khỏi bế tắc.
- **Tận dụng DevTools:** Soi kỹ từng Request, Cookie và Response trả về.
- **Kiên nhẫn biến đổi Payload:** Một payload XSS có thể bị chặn, hãy thử Encode hoặc dùng cú pháp khác.
- **SQLi:** Hãy luôn bắt đầu với cú pháp kinh điển `' OR '1'='1`. Dùng `--` hoặc `#` để comment code.
- **IDOR:** Nhìn thấy số nguyên (1, 2, 3...) ở URL là phải nhào vào sửa liền.
- **JWT:** Vứt token lên jwt.io để xem nó chứa gì bên trong. Thử đổi `alg` thành `none`.

## ⚠️ Tuyên bố miễn trừ trách nhiệm (Legal Disclaimer)
Tất cả các thử thách này được tạo ra **HOÀN TOÀN VÌ MỤC ĐÍCH GIÁO DỤC**.
- CHỈ thực hành trên hệ thống máy chủ cục bộ hoặc hệ thống mà bạn có văn bản ủy quyền hợp pháp.
- Tuyệt đối KHÔNG sử dụng các kỹ thuật này tấn công các trang web thực tế. Đó là hành vi vi phạm pháp luật.
- Hãy là một Hacker mũ trắng có trách nhiệm!
