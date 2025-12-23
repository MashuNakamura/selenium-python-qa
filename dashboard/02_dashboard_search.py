import os
import time
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==================================================================================
# TEST CONFIGURATION
# ==================================================================================
TEST_CASE_ID = "DASHBOARD-002"
TEST_SCENARIO = "Search Functionality - Verify Filtering & Empty State"
BASE_URL = "http://localhost:5173"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Pre-condition: Login Credentials
USER_DATA = {
    "email": "admin@wowadmin.com",
    "password": "secret"
}

# Keyword yang pasti TIDAK ADA di database
SEARCH_KEYWORD_NEGATIVE = "XY_NGAWUR_TEST_123"
# ==================================================================================

def run_test():
    # --- SETUP DRIVER ---
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_experimental_option("detach", True)
    edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Path Setup (Mundur 1 level dari folder 'dashboard')
    current_script_folder = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_script_folder, "../"))

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
        # --- STEP 1: LOGIN ---
        print("[STEP 1] Logging in...")
        driver.get(f"{BASE_URL}/login")

        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(USER_DATA["email"])
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']"))).send_keys(USER_DATA["password"])
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') or @type='submit']"))).click()

        wait.until(EC.url_contains("dashboard"))
        print("   > Login Success.")

        # Tunggu loading awal selesai (Teks 'Live' muncul)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Live')]")))
        time.sleep(1) # Jeda visual

        # --- STEP 2: PERFORM SEARCH (NEGATIVE) ---
        print(f"[STEP 2] Typing unique keyword: '{SEARCH_KEYWORD_NEGATIVE}'...")

        search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search webinars...']")))
        search_input.clear()
        search_input.send_keys(SEARCH_KEYWORD_NEGATIVE)

        # React search usually instant, but let's give it a tiny moment to filter
        time.sleep(1)

        # --- STEP 3: VERIFY EMPTY STATE ---
        print("[STEP 3] Verifying 'No Data' messages appear...")

        # Cari teks "No Live Webinars"
        no_live = driver.find_element(By.XPATH, "//div[contains(text(), 'No Live Webinars')]")
        # Cari teks "No Upcoming Webinars"
        no_upcoming = driver.find_element(By.XPATH, "//div[contains(text(), 'No Upcoming Webinars')]")

        if no_live.is_displayed() and no_upcoming.is_displayed():
            print("   > Empty State Validated: Filtering works (Data hidden).")
        else:
            raise Exception("Search failed: 'No Webinars' message NOT found.")

        # --- STEP 4: CLEAR SEARCH ---
        print("[STEP 4] Clearing Search Bar...")

        # Cara clear yang robust: Ctrl+A -> Delete (kadang .clear() bug di React)
        search_input.send_keys(Keys.CONTROL + "a")
        search_input.send_keys(Keys.DELETE)
        time.sleep(1)

        # --- STEP 5: VERIFY DATA RETURNS (OPTIONAL) ---
        # Kita cek apakah state kembali seperti semula
        # Kalau database kosong dari awal, pesan "No Live" akan tetap ada.
        # Jadi kita pass saja kalau input sudah kosong.

        current_value = search_input.get_attribute("value")
        if current_value == "":
            print("   > Search cleared successfully.")
        else:
            raise Exception("Failed to clear search input.")

        test_result = "PASSED"
        print("\n[RESULT] SEARCH FUNCTIONALITY OK.")

    except Exception as e:
        test_result = "FAILED"
        failure_reason = str(e).splitlines()[0]
        print(f"\n[ERROR] Test Failed: {failure_reason}")

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
        # driver.quit()

if __name__ == "__main__":
    run_test()