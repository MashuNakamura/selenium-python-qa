# 🤖 Selenium Automation Testing Suite – Webinar Platform

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium)
![Test Status](https://img.shields.io/badge/Status-96%25_PASSED-brightgreen?style=for-the-badge)

---

## 📖 Overview

Repository ini berisi rangkaian **Automated Black-box Testing** untuk aplikasi web manajemen **Webinar**.  
Pengujian dilakukan menggunakan **Python** dan **Selenium WebDriver** untuk memvalidasi:

- Fungsionalitas utama (Functional Testing)
- Validasi input & error handling (Negative Testing)
- Keamanan dasar (Security Testing)
- Antarmuka pengguna (UI/UX Testing)

Aplikasi target dibangun menggunakan **React (Frontend)** dan **Go (Backend)** yang dijalankan secara lokal. 

---

## 🚀 Tech Stack

- **Language:** Python 3.10+
- **Automation Tool:** Selenium WebDriver
- **Browser Driver:** Microsoft Edge Driver (`msedgedriver.exe`)
- **Target Application:** React + Go  
- **Base URL:** `http://localhost:5173`
- **Reporting:** CSV (`test_report.csv`)

---

## 🛠️ Installation & Setup

### Clone Repository

```bash
git clone https://github.com/MashuNakamura/selenium-python-qa.git
cd selenium-python-qa
```

### Install Dependencies

Pastikan Python sudah terinstall, lalu jalankan:

```bash
pip install -r requirements.txt
```

### Setup WebDriver

- Pastikan `msedgedriver.exe` tersedia di root folder project
- Versi driver harus sesuai dengan Microsoft Edge yang terinstall
- Jika menggunakan Chrome, ganti dengan `chromedriver.exe` dan sesuaikan konfigurasi driver di script

### Menjalankan Aplikasi Target

- Jalankan backend & frontend aplikasi webinar
- Pastikan aplikasi dapat diakses melalui: 
👉 `http://localhost:5173`

---

## 🧪 Test Scenarios Coverage

Total terdapat **27 Test Cases** yang mencakup positive, negative, functional, security, dan UI/UX testing. 

| Module | Test Case ID | Scenario Description | Type |
|--------|-------------|---------------------|------|
| **Registration** | REG-001 | User Registration with Valid Data | Positive |
|  | REG-002 | Register Failed – Password Mismatch | Negative |
|  | REG-003 | Register Failed – Invalid OTP Code | Negative |
|  | REG-004 | Register Failed – Duplicate Email | Negative |
| **Login** | LOG-001 | Login Success – Valid Admin Credentials | Positive |
|  | LOG-002 | Login Failed – Incorrect Password | Negative |
|  | LOG-003 | Login Failed – Unregistered Email | Negative |
|  | LOG-004 | Login Failed – Invalid Email Format | Negative |
|  | LOG-005 | Login Failed – Empty Fields | Negative |
| **Logout** | LOGOUT-001 | Logout Success – User Initiated | Functional |
| **About Page** | ABOUT-001 | Guest Access – Verify About Page Content | UI/UX |
| **Dashboard** | DASHBOARD-001 | Dashboard Render – Verify Sections & Search | UI/UX |
|  | DASHBOARD-002 | Search Functionality – Verify Filtering | Functional |
|  | DASHBOARD-003 | Pagination Interaction – Rows Per Page | Functional |
| **Forgot Password** | AUTH-FORGOT-001 | Forgot Password Flow – Request OTP | Functional |
|  | AUTH-FORGOT-002 | Forgot Password – Empty Email Validation | Negative |
|  | AUTH-FORGOT-003 | Forgot Password – Unregistered Email | Negative |
| **Profile** | PROF-001 | Edit Profile – Update Name & Instance | Positive |
|  | PROF-002 | Edit Profile – Empty Name Validation | Negative |
|  | PROF-003 | Profile – Navigate to Change Password Page | Functional |
| **Security (Change Password)** | CPASS-001 | Change Password – Success | Security |
|  | CPASS-002 | Change Password – Mismatch Confirmation | Negative |
|  | CPASS-003 | Change Password – Weak Password | Security |
| **History** | HIST-001 | History Webinar – Navigation (User) | Functional |
|  | HIST-002 | History Webinar – Verify UI (User) | UI/UX |

---

## 🏃‍♂️ How to Run Tests

Setiap test case dapat dijalankan secara individual melalui terminal. 

### Contoh Test Login
```bash
python auth/login/01_login_success.py
```

### Contoh Test Dashboard
```bash
python dashboard/01_dashboard_render.py
```

Setiap eksekusi test akan otomatis:
- ✅ Mengukur durasi test
- ✅ Menentukan status **PASSED** / **FAILED**
- ✅ Menyimpan hasil ke file `test_report.csv` (append mode)

---

## 📊 Test Reporting

Hasil pengujian disimpan dalam file CSV (`test_report.csv`) dengan format:

```csv
Date, Time, Test Case ID, Scenario, Duration (s), Result, Failure Reason
2025-12-24, 00:03:59, CPASS-001, Change Password - Success, 2.96, PASSED, -
2025-12-24, 00:05:25, CPASS-002, Change Password - Mismatch Confirmation, 3.01, PASSED, -
2025-12-23, 23:20:28, DASHBOARD-001, Dashboard Render - Verify Sections & Search, 1.30, PASSED, -
```

### Test Result Summary

- **Total Test Cases:** 27
- **Passed:** 26
- **Failed:** 1
- **Success Rate:** ~96%

📌 **Catatan:**  
Test case `AUTH-FORGOT-001` mengalami **FAILED** akibat timeout/error pada proses request OTP, yang kemungkinan dipengaruhi oleh keterlambatan response backend atau konfigurasi email service. 

---

## 📝 Notes & Testing Credentials

Akun yang digunakan dalam pengujian:

**Admin Account:**
- `admin@wowadmin.com`

**User Account:**
- `federicomatthewpratamaa@gmail.com`

**Default Password:**
- `secret` (atau password terakhir yang diubah melalui test Change Password)

---

## 📌 Conclusion

Automation testing ini membuktikan bahwa mayoritas fitur inti aplikasi Webinar berjalan dengan baik dan sesuai ekspektasi.  
Pendekatan **Black-box Testing** menggunakan Selenium efektif dalam mendeteksi error fungsional, validasi input, serta masalah UI/UX pada aplikasi berbasis web modern.
