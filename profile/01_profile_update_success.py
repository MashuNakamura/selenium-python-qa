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
TEST_CASE_ID = "PROF-001"
TEST_SCENARIO = "Edit Profile - Update Name & Instance (Success)"
BASE_URL = "http://localhost:5173"
DRIVER_NAME = "msedgedriver.exe"
REPORT_FILE_NAME = "test_report.csv"

# Credentials
USER_DATA = {
    "email": "admin@wowadmin.com",
    "password": "secret" # Pastikan password ini benar (atau update jika sudah diganti)
}

# Data Baru untuk Update
NEW_PROFILE_DATA = {
    "name": "Admin Ganteng Update",
    "instance": "Universitas Teknologi Test"
}
# ==================================================================================

def run_test():
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    edge_options.add_experimental_option("detach", True)
    edge_options.add_argument("--log-level=3")
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Setup Path (Mundur 1 level dari folder 'profile')
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
        print("[STEP 1] Login...")
        driver.get(f"{BASE_URL}/login")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']"))).send_keys(USER_DATA["email"])
        driver.find_element(By.XPATH, "//input[@type='password']").send_keys(USER_DATA["password"])
        driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        wait.until(EC.url_contains("dashboard"))

        # 2. Navigasi ke Profile
        print("[STEP 2] Navigating to Profile...")
        # Klik Avatar di Navbar -> Klik "My Profile" (sesuai kode Navbar sebelumnya)
        # Atau tembak langsung URL biar cepat:
        driver.get(f"{BASE_URL}/profile")

        # Tunggu loading selesai (Input Full Name muncul)
        # Kita cari input yang labelnya 'Full Name' atau 'Full Name *'
        name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(., 'Full Name')]/following-sibling::div//input | //label[contains(text(), 'Full Name')]/parent::*/following-sibling::*//input | //input[@value]")))
        # Note: Selector HeroUI agak tricky, kita tunggu tombol "Edit Profile" aja yang pasti
        edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Edit Profile')]")))
        print("   > Profile Page Loaded.")

        # 3. Klik Edit Profile
        print("[STEP 3] Enabling Edit Mode...")
        edit_btn.click()
        time.sleep(1) # Animasi

        # 4. Update Data
        print(f"[STEP 4] Updating Name to '{NEW_PROFILE_DATA['name']}'...")

        # Cari Input Name (urutan input biasanya: 1. File(hidden), 2. Name, 3. Email, 4. Instance)
        # Kita pakai XPath index yang aman untuk HeroUI input di form profile ini

        # Input 1 (Name) - pastikan bukan readonly
        inputs = driver.find_elements(By.TAG_NAME, "input")
        # Filter input yang visible saja
        visible_inputs = [i for i in inputs if i.is_displayed()]

        # Asumsi urutan: [0] Search(navbar?), [1] Name, [2] Email, [3] Instance
        # Mari kita cari spesifik parent labelnya

        # Input Name
        name_field = driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'Full Name')]]//input")
        name_field.send_keys(Keys.CONTROL + "a")
        name_field.send_keys(Keys.DELETE)
        name_field.send_keys(NEW_PROFILE_DATA["name"])

        # Input Instance
        instance_field = driver.find_element(By.XPATH, "//div[contains(@class, 'group')][.//label[contains(text(), 'Instance')]]//input")
        instance_field.send_keys(Keys.CONTROL + "a")
        instance_field.send_keys(Keys.DELETE)
        instance_field.send_keys(NEW_PROFILE_DATA["instance"])

        # 5. Save Changes
        print("[STEP 5] Clicking Save Changes...")
        save_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Save Changes')]")
        save_btn.click()

        # 6. Validasi Toast
        print("[STEP 6] Verifying Success Toast...")
        toast_success = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Profile updated successfully')]")))

        if toast_success:
            print("   > Toast 'Profile updated successfully' appeared.")
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