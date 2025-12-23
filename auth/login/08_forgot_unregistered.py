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

TEST_CASE_ID = "AUTH-FORGOT-003"
TEST_SCENARIO = "Forgot Password - Unregistered Email"
TARGET_URL = "http://localhost:5173/login"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Email Ngawur
INVALID_EMAIL = "hantubelau@tidakada.com"

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

        # 1. Navigasi
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Forgot Password')]"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Recovery Account')]")))

        # 2. Input Email Ngawur
        print(f"[STEP 2] Inputting unregistered email: {INVALID_EMAIL}")
        driver.find_element(By.XPATH, "//input[@type='email']").send_keys(INVALID_EMAIL)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Send OTP')]").click()

        # 3. Validasi Error
        print("[STEP 3] Waiting for API response & Error Message...")
        # React Logic: setError("Email is not registered. Please register first.");
        error_msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'text-red-500')]")))

        print(f"   > Error Found: '{error_msg.text}'")

        # Cek potongan kata kuncinya saja biar aman
        if "not registered" in error_msg.text:
            test_result = "PASSED"
        else:
            test_result = "FAILED"
            failure_reason = f"Expected 'not registered', got: {error_msg.text}"

    except Exception as e:
        test_result = "FAILED"
        failure_reason = str(e).splitlines()[0]
        print(f"\n[ERROR] {failure_reason}")

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