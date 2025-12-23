import os
import time
import datetime
import csv  # <-- Library buat Excel/CSV
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==================================================================================
# TEST CONFIGURATION
# ==================================================================================
TEST_CASE_ID = "REG-001"
TEST_SCENARIO = "User Registration with Valid Data (Success)"
TARGET_URL = "http://localhost:5173/register"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv" # Nama file laporannya

# Test Data
USER_DATA = {
    "name": "Federico QA",
    "email": "federicomatthewpratamaa@gmail.com",
    "instance": "DK University",
    "password": "Password123!"
}
# ==================================================================================

def run_test():
    # --- SETUP CONFIGURATION ---
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_experimental_option("detach", True)
    edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # --- PATH SETUP (Driver & Report) ---
    current_script_folder = os.path.dirname(os.path.abspath(__file__))
    # Naik 2 level ke Project Root
    project_root = os.path.abspath(os.path.join(current_script_folder, "../../"))

    driver_path = os.path.join(project_root, DRIVER_NAME)
    report_csv_path = os.path.join(project_root, REPORT_FILE_NAME) # File CSV ditaruh di Root

    if not os.path.exists(driver_path):
        print(f"[CRITICAL ERROR] Driver not found at: {driver_path}")
        return

    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    wait = WebDriverWait(driver, 15)

    # Reporting Variables
    start_time = datetime.datetime.now()
    test_result = "PENDING"
    failure_reason = "-"

    print("\n" + "="*50)
    print(f"STARTING TEST: {TEST_CASE_ID}")
    print("="*50 + "\n")

    try:
        # STEP 1: Navigate
        print(f"[STEP 1] Navigating to {TARGET_URL}...")
        driver.get(TARGET_URL)

        # STEP 2: Fill Form
        print("[STEP 2] Filling personal information form...")
        driver.find_element(By.XPATH, "(//input[@type='text'])[1]").send_keys(USER_DATA["name"])
        driver.find_element(By.XPATH, "//input[@type='email']").send_keys(USER_DATA["email"])
        driver.find_element(By.XPATH, "(//input[@type='text'])[2]").send_keys(USER_DATA["instance"])
        driver.find_element(By.XPATH, "(//input[@type='password'])[1]").send_keys(USER_DATA["password"])
        driver.find_element(By.XPATH, "(//input[@type='password'])[2]").send_keys(USER_DATA["password"])

        # STEP 3: OTP Request
        print("[STEP 3] Requesting OTP Code...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send')]"))).click()

        # --- MANUAL INPUT ---
        print("\n" + "*"*50)
        print("ACTION REQUIRED: Input OTP from Email.")
        print("*"*50)
        otp_code = input(">>> ENTER OTP CODE: ")
        # --------------------

        # STEP 4: Input OTP
        print(f"\n[STEP 4] Inputting OTP...")
        driver.find_element(By.XPATH, "//input[contains(@autocomplete, 'one-time-code')]").send_keys(otp_code)

        # STEP 5: Submit
        print("[STEP 5] Clicking Register Button...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Register']"))).click()

        # STEP 6: Assert
        print("[STEP 6] Verifying success...")
        wait.until(EC.url_contains("login"))

        test_result = "PASSED"
        print("   > Redirected to Login page successfully.")

    except Exception as e:
        test_result = "FAILED"
        failure_reason = str(e).splitlines()[0]
        print(f"\n[ERROR] Test Failed: {failure_reason}")

    finally:
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()

        # ==================================================================================
        # AUTO-GENERATE CSV REPORT
        # ==================================================================================
        file_exists = os.path.isfile(report_csv_path)

        try:
            with open(report_csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)

                # Kalau file baru dibuat, bikin Header dulu
                if not file_exists:
                    writer.writerow(["Date", "Test Case ID", "Scenario", "Duration (s)", "Result", "Failure Reason"])

                # Tulis Data Baris Baru
                writer.writerow([
                    start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    TEST_CASE_ID,
                    TEST_SCENARIO,
                    f"{duration:.2f}",
                    test_result,
                    failure_reason
                ])

            print("\n" + "="*50)
            print(f"REPORT SAVED TO: {report_csv_path}")
            print("="*50 + "\n")

        except Exception as e:
            print(f"⚠️ Gagal menulis CSV (Mungkin file sedang dibuka?): {e}")

        # driver.quit()

if __name__ == "__main__":
    run_test()