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

TEST_CASE_ID = "LOG-004"
TEST_SCENARIO = "Login Failed - Invalid Email Format"
TARGET_URL = "http://localhost:5173/login"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Test Data (Format Email Salah)
USER_DATA = {
    "email": "inivalidemail", # Gak ada @ atau .com
    "password": "AnyPassword"
}

def run_test():
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_experimental_option("detach", True)
    edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    current_script_folder = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_script_folder, "../../"))
    driver_path = os.path.join(project_root, DRIVER_NAME)
    report_csv_path = os.path.join(project_root, REPORT_FILE_NAME)

    if not os.path.exists(driver_path): return

    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    wait = WebDriverWait(driver, 10)

    start_time = datetime.datetime.now()
    test_result = "PENDING"
    failure_reason = "-"

    print("\n" + "="*50)
    print(f"STARTING TEST: {TEST_CASE_ID}")
    print("="*50 + "\n")

    try:
        driver.get(TARGET_URL)
        print("[STEP 2] Inputting Invalid Email Format...")

        driver.find_element(By.XPATH, "//input[@type='email']").send_keys(USER_DATA["email"])
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(USER_DATA["password"])

        print("[STEP 3] Clicking Login Button...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))).click()

        print("[STEP 4] Verifying Error Message...")
        try:
            # Expecting: "Invalid Email" (Case 3)
            # Note: Browser might block submission first (HTML5 validation).
            # If browser blocks, Selenium might throw TimeoutException here.
            error_element = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//*[contains(@class, 'text-red-500') or contains(@class, 'Toastify__toast')]")
            ))

            error_text = error_element.text
            print(f"   > Error Message: '{error_text}'")

            if "Invalid" in error_text:
                test_result = "PASSED"
            else:
                test_result = "FAILED"
                failure_reason = f"Unexpected error text: {error_text}"

        except:
            # Check if we are still on login page (Browser validation blocked it -> PASS)
            if "login" in driver.current_url:
                test_result = "PASSED"
                print("   > Browser Native Validation blocked submission (PASS).")
            else:
                test_result = "FAILED"
                failure_reason = "System logged in with bad email format!"

    except Exception as e:
        test_result = "FAILED"
        failure_reason = str(e).splitlines()[0]

    finally:
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        try:
            with open(report_csv_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([start_time.strftime("%Y-%m-%d %H:%M:%S"), TEST_CASE_ID, TEST_SCENARIO, f"{duration:.2f}", test_result, failure_reason])
            print(f"\n[INFO] Report updated.")
        except: pass
        print("="*50 + "\n")

if __name__ == "__main__":
    run_test()