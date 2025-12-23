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
TEST_CASE_ID = "ABOUT-001"
TEST_SCENARIO = "Guest Access - Verify About Page Content"
BASE_URL = "http://localhost:5173"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Tidak butuh USER_DATA karena Guest Mode

# Expected Data
EXPECTED_TEAM = [
    "Federico Matthew Pratama",
    "Fernando Perry",
    "Vincentius Johanes Lwie Jaya"
]
EXPECTED_STACK = ["React", "TypeScript", "Go", "SQLite3"]
# ==================================================================================

def run_test():
    # --- SETUP DRIVER ---
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_experimental_option("detach", True)
    edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Path Setup (Mundur 1 level dari folder 'about' ke root)
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
        # --- STEP 1: OPEN LANDING PAGE ---
        print("[STEP 1] Opening Landing Page (Guest Mode)...")
        driver.get(BASE_URL)

        # Tunggu Navbar muncul (Indikasi halaman load)
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "nav")))
        print("   > Landing Page Loaded.")

        # --- STEP 2: NAVIGATE TO ABOUT ---
        print("[STEP 2] Clicking 'About' on Navbar...")

        # Cari link "About" di Navbar dan klik
        # Sesuai code navbar: <Link to="/about">About</Link>
        # Selector ini aman karena link About selalu ada baik Guest maupun User
        about_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/about']")))
        about_link.click()

        # Tunggu URL berubah
        wait.until(EC.url_contains("/about"))
        print("   > Successfully navigated to /about")
        time.sleep(1) # Jeda visual sedikit

        # --- STEP 3: VERIFY TITLE ---
        print("[STEP 3] Verifying Page Title...")
        # Mencari H1 yang spesifik
        page_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'About Our Project')]")))
        print("   > Title 'About Our Project' found.")

        # --- STEP 4: VERIFY TEAM MEMBERS ---
        print("[STEP 4] Verifying Team Members...")

        page_source = driver.page_source

        for member in EXPECTED_TEAM:
            if member in page_source:
                print(f"   > Member found: {member}")
            else:
                # Jika nama tidak ketemu, test langsung gagal
                raise Exception(f"Member NOT found: {member}")

        # --- STEP 5: VERIFY TECH STACK ---
        print("[STEP 5] Verifying Tech Stack...")

        for stack in EXPECTED_STACK:
            # Mencari elemen visual badge tech stack
            # Bisa pakai text contains saja biar fleksibel
            try:
                driver.find_element(By.XPATH, f"//*[contains(text(), '{stack}')]")
                print(f"   > Tech Stack found: {stack}")
            except:
                raise Exception(f"Tech Stack NOT found: {stack}")

        test_result = "PASSED"
        print("\n[RESULT] ALL CHECKS PASSED.")

    except Exception as e:
        test_result = "FAILED"
        failure_reason = str(e).splitlines()[0]
        print(f"\n[ERROR] Test Failed: {failure_reason}")
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
        # driver.quit()

if __name__ == "__main__":
    run_test()