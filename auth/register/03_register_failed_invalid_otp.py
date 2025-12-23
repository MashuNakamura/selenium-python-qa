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
TEST_CASE_ID = "REG-003"
TEST_SCENARIO = "Register Failed - Invalid OTP Code"
TARGET_URL = "http://localhost:5173/register"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Test Data (Valid User Data, but we will use INVALID OTP)
USER_DATA = {
    "name": "Federico Invalid OTP",
    "email": "federico_wrong_otp@test.com",
    "instance": "Test Instance",
    "password": "Password123!"
}
INVALID_OTP = "000000" # Hardcoded wrong OTP
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
    wait = WebDriverWait(driver, 15)

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

        # STEP 2: Fill Form (Valid Data)
        print("[STEP 2] Filling form with valid personal data...")
        driver.find_element(By.XPATH, "(//input[@type='text'])[1]").send_keys(USER_DATA["name"])
        driver.find_element(By.XPATH, "//input[@type='email']").send_keys(USER_DATA["email"])
        driver.find_element(By.XPATH, "(//input[@type='text'])[2]").send_keys(USER_DATA["instance"])
        driver.find_element(By.XPATH, "(//input[@type='password'])[1]").send_keys(USER_DATA["password"])
        driver.find_element(By.XPATH, "(//input[@type='password'])[2]").send_keys(USER_DATA["password"])

        # STEP 3: Request OTP (To activate the field)
        print("[STEP 3] Requesting OTP Code...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Send')]"))).click()

        # Wait slightly to simulate network delay
        time.sleep(2)

        # STEP 4: Input INVALID OTP
        print(f"[STEP 4] Inputting INVALID OTP: {INVALID_OTP}...")
        # No manual input needed here!
        otp_input = driver.find_element(By.XPATH, "//input[contains(@autocomplete, 'one-time-code')]")
        otp_input.send_keys(INVALID_OTP)

        # STEP 5: Click Register
        print("[STEP 5] Clicking Register Button...")
        register_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Register']")))
        register_btn.click()

        # STEP 6: Assert Error Message
        print("[STEP 6] Verifying Rejection...")

        # We expect an error containing "Invalid" or "expired"
        try:
            # Wait for Toast or Error Text
            error_element = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Invalid') or contains(text(), 'expired')]")
            ))

            print(f"   > Error Message Found: '{error_element.text}'")
            test_result = "PASSED"

        except:
            if "login" in driver.current_url:
                test_result = "FAILED"
                failure_reason = "System ACCEPTED an invalid OTP (Critical Security Bug)"
            else:
                test_result = "FAILED"
                failure_reason = "Expected error 'Invalid OTP' did not appear."

    except Exception as e:
        test_result = "FAILED"
        failure_reason = str(e).splitlines()[0]
        print(f"\n[ERROR] Exception: {failure_reason}")

    finally:
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()

        # ==================================================================================
        # AUTO-GENERATE CSV REPORT
        # ==================================================================================
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
            print(f"\n[INFO] Report updated in: {report_csv_path}")

        except Exception as e:
            print(f"⚠️ Failed to write CSV: {e}")

        print("="*50 + "\n")
        # driver.quit()

if __name__ == "__main__":
    run_test()