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
TEST_CASE_ID = "HIST-001"
TEST_SCENARIO = "History Webinar - Navigation via Avatar Dropdown (User)"
BASE_URL = "http://localhost:5173"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# KITA PAKAI AKUN USER (Bukan Admin)
USER_DATA = {
    "email": "federicomatthewpratamaa@gmail.com",
    "password": "Password123!" # <--- GANTI SESUAI PASSWORD AKUN INI
}
# ==================================================================================

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
        # 1. Login User
        print(f"[STEP 1] Login as {USER_DATA['email']}...")
        driver.get(f"{BASE_URL}/login")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(USER_DATA["email"])
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(USER_DATA["password"])
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        wait.until(EC.url_contains("dashboard"))

        # 2. Klik Avatar
        print("[STEP 2] Clicking Avatar...")
        avatar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//header//button[.//img]")))
        avatar_btn.click()

        # 3. Klik Menu History Webinar
        print("[STEP 3] Clicking 'History Webinar'...")
        # Menu ini harusnya muncul untuk role User
        history_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'History Webinar')] | //div[contains(text(), 'History Webinar')]")))
        history_menu.click()

        # 4. Validasi Halaman
        print("[STEP 4] Validating History Page...")

        # Cek URL ada kata 'history'
        wait.until(EC.url_contains("history"))

        # Cek Judul Halaman (H1)
        h1_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'History Webinar')]")))

        if h1_title.is_displayed():
            print(f"   > Successfully landed on: {driver.current_url}")
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