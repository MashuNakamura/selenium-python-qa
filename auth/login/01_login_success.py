import os
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Server Configuration
# -----------------------------------------------
TARGET_URL = "http://localhost:5173/login"
DRIVER_NAME = "msedgedriver.exe"
# -----------------------------------------------

# Main Test Function
def run_test():
    # Setup Edge Driver
    edge_options = Options() # Using Edge Options
    edge_options.add_argument("--start-maximized") # Open Browser in Maximized Mode
    edge_options.add_experimental_option("detach", True) # Keep the browser open after script ends
    edge_options.add_argument("--log-level=3") # Show only fatal errors
    edge_options.add_experimental_option('excludeSwitches', ['enable-logging']) # Disable Logging

    # Attach Driver Service and Read From Current Folder
    current_folder = os.path.dirname(os.path.abspath(__file__))
    driver_path = os.path.join(current_folder, DRIVER_NAME)
    service = Service(driver_path)

    # Initialize WebDriver
    print(f"[INIT] Opening Edge Browser...")
    driver = webdriver.Edge(service=service, options=edge_options) # Start Edge Driver
    wait = WebDriverWait(driver, 10) # 10 seconds wait time

    try:
        # Start Testing Steps

        # Open Website
        print(f"[PROCESS] Opening Target URL: {TARGET_URL}...")
        driver.get(TARGET_URL) # Open Target URL

        # STEP 2: Input Email
        print("[PROCESS] Input Email...")
        # Wait until the email input is visible
        # email_input = wait.until(EC.visibility_of_element_located((By.NAME, "email")))
        email_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input")))
        email_input.clear() # Clear any pre-filled text
        email_input.send_keys("admin@wowadmin.com") # Input Email

        # STEP 3: Input Password
        print("[PROCESS] Input Password...")
        # No need to wait again, just find the password input
        # pass_input = driver.find_element(By.NAME, "password")
        pass_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
        pass_input.clear() # Clear any pre-filled text
        pass_input.send_keys("secret") # Input Password

        # STEP 4: Login
        print("[PROCESS] Searching Login Button...")
        # Search for the login button and click it
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]")))
        login_btn.click()

        # STEP 5: Validate Dashboard URL
        print("[PROCESS] Validating Dashboard URL...")
        wait.until(EC.url_contains("dashboard"))

        # Report Success or Failure
        print("-" * 30)
        print("[PASSED] Test Successful!")
        print(f" Last Position: {driver.current_url}")
        print("-" * 30)

    except Exception as e:
        print("-" * 30)
        print("[FAILED] Failed to complete the test.")
        print(f"Reason: {e}")
        print("-" * 30)

    finally:
        print("[FINISH] Test Completed.")
        driver.quit() # Quit the driver after test

if __name__ == "__main__":
    run_test()