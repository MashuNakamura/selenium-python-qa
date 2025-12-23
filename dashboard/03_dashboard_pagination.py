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
from selenium.webdriver.support.ui import Select

# ==================================================================================
# TEST CONFIGURATION
# ==================================================================================
TEST_CASE_ID = "DASHBOARD-003"
TEST_SCENARIO = "Pagination Interaction - Rows Per Page & Next Button"
BASE_URL = "http://localhost:5173"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Pre-condition: Login Credentials
USER_DATA = {
    "email": "admin@wowadmin.com",
    "password": "secret"
}
# ==================================================================================

def run_test():
    # --- SETUP DRIVER ---
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_experimental_option("detach", True)
    edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

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

        # Tunggu loading selesai
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Live')]")))
        time.sleep(1)

        # --- STEP 2: TEST ROWS PER PAGE DROPDOWN ---
        print("[STEP 2] Testing 'Rows per page' Dropdown...")

        # Cari elemen <select> pertama (biasanya punya bagian Live)
        select_element = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "select")))

        # Gunakan class Select dari Selenium untuk interaksi mudah
        dropdown = Select(select_element)

        # Cek default value (biasanya 5)
        default_val = dropdown.first_selected_option.text
        print(f"   > Default selection: {default_val}")

        # Ubah ke '10'
        print("   > Changing selection to '10 / page'...")
        dropdown.select_by_value("10") # Sesuai value={opt} di React
        time.sleep(1)

        # Validasi perubahan
        current_val = dropdown.first_selected_option.text
        if "10" in current_val:
            print("   > Dropdown updated successfully.")
        else:
            raise Exception(f"Dropdown failed to update. Current: {current_val}")

        # --- STEP 3: CONDITIONAL TEST NEXT BUTTON ---
        print("[STEP 3] Checking 'Next' Button capability...")

        # Cari tombol Next yang ada di dekat dropdown tadi
        # XPath: Cari tombol yang tulisannya 'Next'
        next_btn = driver.find_element(By.XPATH, "//button[text()='Next']")

        # Cek apakah disabled?
        is_disabled = next_btn.get_attribute("disabled")

        if is_disabled:
            print("   > 'Next' button is DISABLED (Not enough data).")
            print("   > [INFO] Skipping click test. This is expected behavior for small datasets.")
        else:
            print("   > 'Next' button is ENABLED. Clicking it...")
            next_btn.click()
            time.sleep(1)

            # Validasi Page berubah
            # Cari teks "Page 2" di span dekat tombol
            page_indicator = driver.find_element(By.XPATH, "//span[contains(text(), 'Page 2')]")
            if page_indicator.is_displayed():
                print("   > Successfully moved to Page 2.")
            else:
                raise Exception("Clicked Next but page indicator did not update.")

        test_result = "PASSED"
        print("\n[RESULT] PAGINATION CONTROLS OK.")

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