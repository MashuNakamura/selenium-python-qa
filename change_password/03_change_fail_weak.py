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

TEST_CASE_ID = "CPASS-003"
TEST_SCENARIO = "Change Password - Weak Password (Fail)"
BASE_URL = "http://localhost:5173"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Credentials Saat Ini
CURRENT_PASS = "MakanNasi123!"

def run_test():
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_experimental_option("detach", True)
    edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    current_script_folder = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_script_folder, "../"))
    driver_path = os.path.join(project_root, DRIVER_NAME)
    report_csv_path = os.path.join(project_root, REPORT_FILE_NAME)

    if not os.path.exists(driver_path): return
    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    wait = WebDriverWait(driver, 15)
    start_time = datetime.datetime.now()
    test_result = "PENDING"
    failure_reason = "-"

    print("\n" + "="*50)
    print(f"STARTING TEST: {TEST_CASE_ID}")
    print("="*50 + "\n")

    try:
        # 1. Login
        print(f"[STEP 1] Login with: {CURRENT_PASS}...")
        driver.get(f"{BASE_URL}/login")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys("admin@wowadmin.com")
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(CURRENT_PASS)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        wait.until(EC.url_contains("dashboard"))

        # 2. Navigasi
        print("[STEP 2] Navigating to Change Password...")
        driver.get(f"{BASE_URL}/profile")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Edit Profile')]"))).click()
        time.sleep(0.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Change Password')]"))).click()

        # 3. Input Weak Password
        print("[STEP 3] Inputting Weak Password (No Uppercase)...")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'CHANGE PASSWORD')]")))

        # Old Pass
        driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'Old Password')]]//input").send_keys(CURRENT_PASS)

        # New Pass: "lemah123" (Kurang huruf besar)
        driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'New Password')]]//input").send_keys("lemah123")

        # Confirm Pass: "lemah123"
        driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'Confirm New Password')]]//input").send_keys("lemah123")

        # 4. Submit
        driver.find_element(By.XPATH, "//button[@type='submit'][contains(text(), 'Change Password')]").click()

        # 5. Validasi Error Toast
        print("[STEP 4] Verifying Regex Error Toast...")
        # React Code: toast.warning("New password must be at least 8 characters long...")
        # Kita cari potongan teks uniknya
        error_toast = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'at least 8 characters') or contains(text(), 'uppercase')]")))

        if error_toast:
            print(f"   > Error Toast Found: '{error_toast.text}'")
            test_result = "PASSED"

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
        except: pass
        print("="*50 + "\n")

if __name__ == "__main__":
    run_test()