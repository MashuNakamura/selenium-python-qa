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

TEST_CASE_ID = "PROF-003"
TEST_SCENARIO = "Change Password Flow - Update & Redirect"
BASE_URL = "http://localhost:5173"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Current Credentials
CURRENT_PASS = "secret"
# New Credentials to Set
NEW_PASS = "NewPass1!" # Memenuhi syarat strong password (Huruf besar, kecil, angka, simbol)

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
        print("[STEP 1] Login with current password...")
        driver.get(f"{BASE_URL}/login")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys("admin@wowadmin.com")
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(CURRENT_PASS)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        wait.until(EC.url_contains("dashboard"))

        # 2. Go to Profile & Click Change Password
        print("[STEP 2] Going to Change Password Page...")
        driver.get(f"{BASE_URL}/profile")

        change_pass_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Change Password')]")))
        change_pass_btn.click()

        # 3. Validasi URL
        wait.until(EC.url_contains("change-password"))
        print("   > Landed on Change Password Page.")

        # 4. Input Form
        print(f"[STEP 3] Changing password to '{NEW_PASS}'...")

        # Input 1: Old Password
        # Cari input berdasarkan label terdekat
        old_pass_input = driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'Old Password')]]//input")
        old_pass_input.send_keys(CURRENT_PASS)

        # Input 2: New Password
        new_pass_input = driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'New Password')]]//input")
        new_pass_input.send_keys(NEW_PASS)

        # Input 3: Confirm Password
        confirm_pass_input = driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'Confirm New Password')]]//input")
        confirm_pass_input.send_keys(NEW_PASS)

        # 5. Submit
        print("[STEP 4] Submitting form...")
        # Cari tombol Change Password (hati-hati jangan ketukar sama judul H1)
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit'][contains(text(), 'Change Password')]")
        submit_btn.click()

        # 6. Validasi Redirect ke Profile
        print("[STEP 5] Waiting for redirect back to Profile...")
        wait.until(EC.url_contains("profile"))

        # Validasi Toast Success
        success_toast = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Password changed successfully')]")))

        if success_toast:
            print("   > Password Change Success! Redirected to Profile.")
            print(f"   > [IMPORTANT] Your Admin password is now: {NEW_PASS}")
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