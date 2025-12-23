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
TEST_CASE_ID = "LOG-002"
TEST_SCENARIO = "Login Failed - Incorrect Password"
TARGET_URL = "http://localhost:5173/login"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Test Data (Email Valid, Password SALAH)
USER_DATA = {
    "email": "admin@wowadmin.com",
    "password": "WrongPassword123!"
}
# ==================================================================================

def run_test():
    # --- CONFIGURATION & PATHS ---
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
    wait = WebDriverWait(driver, 10)

    # Reporting Variables
    start_time = datetime.datetime.now()
    test_result = "PENDING"
    failure_reason = "-"

    print("\n" + "="*50)
    print(f"STARTING TEST: {TEST_CASE_ID}")
    print(f"SCENARIO: {TEST_SCENARIO}")
    print("="*50 + "\n")

    try:
        # STEP 1: Navigate
        print(f"[STEP 1] Navigating to {TARGET_URL}...")
        driver.get(TARGET_URL)

        # STEP 2: Input Credentials
        print("[STEP 2] Inputting Valid Email & Wrong Password...")

        driver.find_element(By.XPATH, "//input[@type='email']").send_keys(USER_DATA["email"])

        pass_input = driver.find_element(By.XPATH, "//input[@type='password']")
        pass_input.send_keys(USER_DATA["password"])

        # STEP 3: Click Login
        print("[STEP 3] Clicking Login Button...")
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_btn.click()

        # STEP 4: Verify Error Message
        print("[STEP 4] Verifying Error Message...")

        try:
            # Cari Error Text (Merah) ATAU Toast Warning (Kuning/Merah)
            # Sesuai React Mas: toast.warn("Password is Incorrect")
            error_element = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@class, 'text-red-500') or contains(@class, 'Toastify__toast')]")
            ))

            error_text = error_element.text
            print(f"   > Error Message Detected: '{error_text}'")

            # Assertion Logic
            if "Incorrect" in error_text or "Password" in error_text:
                test_result = "PASSED"
            else:
                test_result = "FAILED"
                failure_reason = f"Unexpected error message: {error_text}"

        except:
            if "dashboard" in driver.current_url:
                test_result = "FAILED"
                failure_reason = "System LOGGED IN with wrong password! (Critical Bug)"
            else:
                test_result = "FAILED"
                failure_reason = "No error message appeared."

    except Exception as e:
        test_result = "FAILED"
        failure_reason = str(e).splitlines()[0]
        print(f"\n[ERROR] Exception: {failure_reason}")

    finally:
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Write to CSV
        try:
            file_exists = os.path.isfile(report_csv_path)
            with open(report_csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Date", "Test Case ID", "Scenario", "Duration (s)", "Result", "Failure Reason"])
                writer.writerow([start_time.strftime("%Y-%m-%d %H:%M:%S"), TEST_CASE_ID, TEST_SCENARIO, f"{duration:.2f}", test_result, failure_reason])
            print(f"\n[INFO] Report updated in: {report_csv_path}")
        except Exception as e:
            print(f"⚠️ Failed to write CSV: {e}")

        print("="*50 + "\n")
        # driver.quit()

if __name__ == "__main__":
    run_test()