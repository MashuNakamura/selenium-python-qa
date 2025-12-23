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

TEST_CASE_ID = "CPASS-001"
TEST_SCENARIO = "Change Password - Success (Validation by Redirect)"
BASE_URL = "http://localhost:5173"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# ==============================================================================
# CREDENTIALS CONFIGURATION
# ==============================================================================
# Asumsi password saat ini adalah hasil dari tes sebelumnya
OLD_PASS = "Secret123!"

# Password BARU yang akan diset sekarang
NEW_PASS = "MakanNasi123!"
# ==============================================================================

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
        # 1. Login dengan Password SAAT INI
        print(f"[STEP 1] Login with current password: {OLD_PASS}...")
        driver.get(f"{BASE_URL}/login")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys("admin@wowadmin.com")
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(OLD_PASS)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()

        # Tunggu masuk dashboard
        wait.until(EC.url_contains("dashboard"))

        # 2. Navigasi ke Change Password
        print("[STEP 2] Navigating to Change Password...")
        driver.get(f"{BASE_URL}/profile")

        # Klik Edit Profile dulu
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Edit Profile')]"))).click()
        time.sleep(0.5)
        # Klik Change Password
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Change Password')]"))).click()

        # 3. Isi Form Password
        print(f"[STEP 3] Changing password to: {NEW_PASS}...")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'CHANGE PASSWORD')]")))

        # Old Pass
        driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'Old Password')]]//input").send_keys(OLD_PASS)
        # New Pass
        driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'New Password')]]//input").send_keys(NEW_PASS)
        # Confirm Pass
        driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'Confirm New Password')]]//input").send_keys(NEW_PASS)

        # 4. Submit
        print("[STEP 4] Submitting form...")
        driver.find_element(By.XPATH, "//button[@type='submit'][contains(text(), 'Change Password')]").click()

        # 5. Validasi Akhir (Cukup Redirect ke Profile)
        print("[STEP 5] Verifying Redirect to Profile...")

        # Kita tunggu URL mengandung 'profile' DAN pastikan TIDAK mengandung 'change-password' lagi
        wait.until(EC.url_matches(f"{BASE_URL}/profile"))

        # Double check URL aktual
        current_url = driver.current_url
        if "profile" in current_url and "change-password" not in current_url:
            print("   > Redirected to Profile Page confirmed.")
            print(f"   > [INFO] Password updated successfully to: {NEW_PASS}")
            test_result = "PASSED"
        else:
            raise Exception(f"Redirect failed. Stuck at: {current_url}")

    except Exception as e:
        test_result = "FAILED"
        failure_reason = str(e).splitlines()[0]
        print(f"\n[ERROR] {failure_reason}")
        print("[HINT] Jika error di Login, coba ganti OLD_PASS di script jadi password sebelumnya.")

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