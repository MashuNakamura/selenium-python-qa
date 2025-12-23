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
TEST_CASE_ID = "LOGOUT-001"
TEST_SCENARIO = "Logout Success - User Initiated"
BASE_URL = "http://localhost:5173"  # Pastikan port frontend benar
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Pre-condition Data
USER_DATA = {
    "email": "admin@wowadmin.com",
    "password": "secret"
}
# ==================================================================================

def run_test():
    # --- CONFIGURATION & PATHS ---
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_experimental_option("detach", True)
    edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Setup Path (Mundur 2 folder untuk cari driver)
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
        # --- PRE-CONDITION: LOGIN ---
        print("[STEP 1] Navigating to Login Page...")
        driver.get(f"{BASE_URL}/login")

        print("[STEP 2] Logging in as Admin...")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(USER_DATA["email"])
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(USER_DATA["password"])
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))).click()

        print("[STEP 3] Waiting for Dashboard...")
        wait.until(EC.url_contains("dashboard"))
        print("   > Login Success. Dashboard loaded.")
        time.sleep(2) # Jeda visual biar UI tenang dulu

        # --- TEST STEPS: LOGOUT ---

        # 1. Klik Avatar (Pojok Kanan Atas di screenshot kamu)
        print("[STEP 4] Clicking Avatar on Navbar...")
        # Cari elemen button di dalam header yang punya gambar(img)
        avatar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//header//button[.//img]")))
        avatar_btn.click()

        # 2. Klik Log Out (Tombol Pink di screenshot)
        print("[STEP 5] Clicking 'Log Out' button...")
        # Cari elemen list (li) yang punya data-key='logout' ATAU text berisi "Log Out"
        logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@data-key='logout'] | //*[contains(text(), 'Log Out')]")))
        logout_btn.click()

        # 3. Validasi Redirect ke Home & Token Hilang
        print("[STEP 6] Validating Logout result...")

        # Cek apakah URL kembali ke halaman awal (Login/Home)
        wait.until(EC.url_to_be(f"{BASE_URL}/"))

        # Cek apakah Token di LocalStorage sudah dihapus
        token = driver.execute_script("return localStorage.getItem('token');")

        if token is None:
            test_result = "PASSED"
            print(f"   > Redirected to Home: YES")
            print(f"   > Token cleared: YES")
        else:
            raise Exception(f"Logout failed. Token still exists: {token}")

    except Exception as e:
        test_result = "FAILED"
        failure_reason = str(e).splitlines()[0]
        print(f"\n[ERROR] Exception: {failure_reason}")
        # driver.save_screenshot(f"evidence_{TEST_CASE_ID}_failed.png")

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
            print(f"\n[INFO] Report updated: {report_csv_path}")

        except Exception as e:
            print(f"⚠️ Failed to write CSV: {e}")

        print("="*50 + "\n")

if __name__ == "__main__":
    run_test()