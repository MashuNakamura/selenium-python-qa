# 🤖 Selenium Automation Testing Suite - Webinar Platform

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium)
![Test Status](https://img.shields.io/badge/Status-96%25_PASSED-brightgreen?style=for-the-badge)

## 📖 Overview

Repository ini berisi rangkaian **Automated Black-box Testing** untuk aplikasi web manajemen Webinar. Project ini dibuat menggunakan **Python** dan **Selenium WebDriver** untuk memvalidasi fungsionalitas utama, keamanan (security), dan antarmuka pengguna (UI/UX).  

Pengujian mencakup berbagai modul kritis seperti **Authentication**, **Dashboard**, **Profile Management**, **Security (Password logic)**, dan **History Participation**.

## 🚀 Tech Stack

- **Language:** Python 3.10+
- **Library:** Selenium
- **Browser Driver:** Microsoft Edge Driver (`msedgedriver.exe`)
- **Target Application:** React + Go (Running on `localhost:5173`)
- **Reporting:** CSV Export

---

## 🛠️ Installation & Setup

### Clone Repository

```bash
git clone https://github.com/username-anda/selenium-webinar-test.git
cd selenium-webinar-test
```

### Install Dependencies

Pastikan Python sudah terinstall, lalu install library Selenium:

```bash
pip install requirements.txt
```

### Setup WebDriver

- Pastikan `msedgedriver.exe` tersedia di root folder dan versinya sesuai dengan browser Microsoft Edge Anda.
- Jika menggunakan Chrome, ganti driver dengan `chromedriver.exe` dan sesuaikan inisialisasi driver di script.

### Target URL Configuration

- Secara default, script menargetkan: [http://localhost:5173](http://localhost:5173).
- Pastikan aplikasi web lokal sudah berjalan sebelum menjalankan test.

---

## 🧪 Test Scenarios Coverage

Total terdapat **25 Test Cases** yang mencakup *positive* dan *negative testing*:

| Module           | Test Case ID   | Scenario Description                                 | Type         |
|------------------|---------------|------------------------------------------------------|--------------|
| **Registration** | REG-001        | User Registration with Valid Data                    | Positive     |
|                  | REG-002        | Register Failed - Password Mismatch                  | Negative     |
|                  | REG-003        | Register Failed - Invalid OTP Code                   | Negative     |
|                  | REG-004        | Register Failed - Duplicate Email                    | Negative     |
| **Login**        | LOG-001        | Login Success - Valid Admin Credentials              | Positive     |
|                  | LOG-002 to 005 | Login Failed (Bad Pass, Unregistered, Format, Empty) | Negative     |
| **Logout**       | LOGOUT-001     | Logout Success & Token Clearing                      | Positive     |
| **Dashboard**    | DASHBOARD-001  | Dashboard Render (Live/Upcoming Sections)            | UI/UX        |
|                  | DASHBOARD-002  | Search Functionality (Real-time Filter)              | Functional   |
|                  | DASHBOARD-003  | Pagination Controls                                 | Functional   |
| **Profile**      | PROF-001       | Edit Profile Success (Update Name & Instance)        | Positive     |
|                  | PROF-002       | Edit Profile Validation (Empty Name)                 | Negative     |
| **Security**     | CPASS-001      | Change Password Success (Strong Regex)               | Security     |
|                  | CPASS-002      | Change Password Fail (Mismatch Confirm)              | Negative     |
|                  | CPASS-003      | Change Password Fail (Weak Password)                 | Security     |
|                  | AUTH-FORGOT-001| Forgot Password Flow & OTP Request                   | Functional   |
| **History**      | HIST-001       | Navigation to History via Avatar                     | Functional   |
|                  | HIST-002       | UI Verification (Search & Empty State)               | UI/UX        |

---

## 🏃‍♂️ How to Run Tests

Anda dapat menjalankan script secara individual menggunakan terminal.

**Contoh menjalankan Test Login:**
```bash
python auth/login/01_login_success.py
```

**Contoh menjalankan Test Dashboard:**
```bash
python dashboard/01_dashboard_render.py
```

Setiap kali script dijalankan, hasilnya akan otomatis dicatat (*append*) ke dalam file `test_report.csv`.

---

## 📊 Reporting

Hasil pengujian disimpan dalam format **CSV** (`test_report.csv`) dengan struktur berikut:

```
Date, Time, Test Case ID, Scenario, Duration (s), Result, Failure Reason
2025-12-24, 00:03:59, CPASS-001, Change Password - Success, 2.96, PASSED, -
2025-12-24, 00:05:25, CPASS-002, Change Password - Mismatch, 3.01, PASSED, -
```

---

## 📝 Notes & Credentials

Akun testing yang digunakan dalam skenario ini:

- **Role Admin:** `admin@wowadmin.com`
- **Role User:** `federicomatthewpratamaa@gmail.com`
- **Default Password:** `secret` *(atau password terakhir yang diupdate oleh script Change Password).*
