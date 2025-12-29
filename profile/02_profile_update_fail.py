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

TEST_CASE_ID = "PROF-002"
TEST_SCENARIO = "Edit Profile - Empty Name Validation (Fail)"
BASE_URL = "http://localhost:5173"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

USER_DATA = { "email": "admin@wowadmin.com", "password": "secret" }

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
        # Login & Go to Profile
        driver.get(f"{BASE_URL}/login")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(USER_DATA["email"])
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(USER_DATA["password"])
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        wait.until(EC.url_contains("dashboard"))

        driver.get(f"{BASE_URL}/profile")
        edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Edit Profile')]")))
        edit_btn.click()

        # Empty the name
        print("[STEP] Emptying Name field...")
        name_field = driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'Full Name')]]//input")
        name_field.send_keys(Keys.CONTROL + "a")
        name_field.send_keys(Keys.DELETE)

        # Save
        print("[STEP] Trying to Save...")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Save Changes')]").click()

        # Verify Validation Toast
        print("[STEP] Verifying Validation Message...")
        # Kodingan React: toast.info("Name cannot be empty")
        toast_msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Name cannot be empty')]")))

        if toast_msg:
            print("   > Correct validation message appeared.")
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