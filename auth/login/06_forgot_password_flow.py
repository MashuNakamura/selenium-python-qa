import os
import time
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==================================================================================
# TEST CONFIGURATION
# ==================================================================================
TEST_CASE_ID = "AUTH-FORGOT-001"
TEST_SCENARIO = "Forgot Password Flow - Request OTP & UI Transitions"
TARGET_URL = "http://localhost:5173/login"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Email yang valid di database (User Admin tadi)
VALID_EMAIL = "federicomatthewpratamaa@gmail.com"
# ==================================================================================

def run_test():
    # --- SETUP DRIVER ---
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_experimental_option("detach", True)
    edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    current_script_folder = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_script_folder, "../../"))

    driver_path = os.path.join(project_root, DRIVER_NAME)
    report_csv_path = os.path.join(project_root, REPORT_FILE_NAME)

    if not os.path.exists(driver_path):
        print(f"[CRITICAL ERROR] Driver not found at: {driver_path}")
        return

    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    wait = WebDriverWait(driver, 15) # Wait agak lama buat nunggu API backend

    # Reporting Variables
    start_time = datetime.datetime.now()
    test_result = "PENDING"
    failure_reason = "-"

    print("\n" + "="*50)
    print(f"STARTING TEST: {TEST_CASE_ID}")
    print(f"SCENARIO: {TEST_SCENARIO}")
    print("="*50 + "\n")

    try:
        # --- STEP 1: OPEN LOGIN PAGE ---
        print("[STEP 1] Opening Login Page...")
        driver.get(TARGET_URL)

        # --- STEP 2: CLICK FORGOT PASSWORD ---
        print("[STEP 2] Clicking 'Forgot Password ?'...")
        # Sesuai code React: <span ...>Forgot Password ?</span>
        forgot_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Forgot Password')]")))
        forgot_btn.click()

        # Validasi Masuk State 'forgot'
        print("   > Waiting for 'Recovery Account' view...")
        # Sesuai code: <h1 ...>Recovery Account</h1>
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Recovery Account')]")))
        print("   > State changed to 'Recovery Account'.")

        # --- STEP 3: INPUT EMAIL & SEND OTP ---
        print("[STEP 3] Inputting Email & Sending OTP...")

        # Cari input email di halaman forgot
        email_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']")))
        email_input.send_keys(VALID_EMAIL)

        # Klik tombol Send OTP
        # Sesuai code: Button text "Send OTP"
        send_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Send OTP')]")
        send_btn.click()

        print("   > 'Send OTP' clicked. Waiting for API response...")

        # --- STEP 4: VERIFY OTP PAGE APPEARS ---
        # Disini kita memastikan backend merespon success dan state pindah ke 'otp'
        print("[STEP 4] Verifying transition to OTP Page...")

        # Sesuai code: setPage("otp") -> render <h1 ...>Enter OTP</h1>
        otp_header = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Enter OTP')]")))

        if otp_header.is_displayed():
            print("   > OTP Sent Successfully! You are now on the OTP Entry screen.")

            # --- OPTIONAL: VALIDATE OTP INPUT EXISTENCE ---
            # Kita cek ada input OTP gak
            otp_input = driver.find_element(By.XPATH, "//div[contains(@data-slot,'input-wrapper')]//input")
            # Note: HeroUI input strukturnya agak dalem, kita cari input generic di page ini
            if otp_input:
                print("   > OTP Input field found.")

            test_result = "PASSED"
        else:
            raise Exception("Failed to reach OTP Page (Maybe API Error/Invalid Email)")

        # NOTE:
        # Kita berhenti disini karena Selenium TIDAK TAHU kode OTP yang dikirim ke email.
        # Kecuali Mas punya "Magic OTP" (misal 123456) buat testing di backend,
        # kita gak bisa lanjut ke step 'Reset Password' secara otomatis.

    except Exception as e:
        test_result = "FAILED"
        failure_reason = str(e).splitlines()[0]
        print(f"\n[ERROR] Test Failed: {failure_reason}")

    finally:
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Update CSV Report
        try:
            file_exists = os.path.isfile(report_csv_path)
            with open(report_csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Date", "Test Case ID", "Scenario", "Duration (s)", "Result", "Failure Reason"])

                writer.writerow([
                    start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    TEST_CASE_ID,
                    TEST_SCENARIO,
                    f"{duration:.2f}",
                    test_result,
                    failure_reason
                ])
            print(f"\n[INFO] Report updated.")
        except Exception as e:
            print(f"⚠️ Failed to write CSV: {e}")

        print("="*50 + "\n")
        # driver.quit()

if __name__ == "__main__":
    run_test()