from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timezone
import subprocess
import platform

load_dotenv()

# Add Discord webhook configuration
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def check_ping(host="10.1.1.1"):
    """
    Returns True if host responds to a ping request, False otherwise.
    """
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def send_discord_notification(message, embeds_color):
    """Send notification to Discord channel"""
    try:
        data = {
            "username": "Airtel Router Reboot (Home Server)",
            "avatar_url": "https://imgcdn.stablediffusionweb.com/2024/10/19/7bfb8866-bc64-4c40-8dba-c83c55fea29f.jpg",
            "embeds": [
                {
                    "title": "Router Reboot Notification",
                    "description": message,
                    "color": embeds_color,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            ]
            # "content": message,
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending Discord notification: {e}")

# Check if router is pingable before proceeding
if not check_ping():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"❌ Router ping failed at {current_time}. Airtel Router is not accessible at 10.1.1.1"
    send_discord_notification(message, 16711680)  # Red color for error
    print(message)
    exit(1)

# Send notification before starting the reboot process
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
send_discord_notification(f"🔄 Router reboot initiated at {current_time}", 255)
print(f"🔄 Router reboot initiated at {current_time}")


options = webdriver.ChromeOptions()
# headless + stealth
options.add_argument('--headless=new')        # Comment this line if you want to see operation in pop-up browser
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-gpu')
options.add_argument(f'--window-size=1920,1080')
options.add_argument('--start-maximized')
options.add_argument('--disable-notifications')
options.add_argument(f'--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

# Navigate to the site
try:
    driver.get("http://10.1.1.1/")
    time.sleep(3)
    driver.save_screenshot("Airtel-1-login_page.png")
except Exception as e:
    print(f"Error opening Router Admin page: {e}")
    send_discord_notification(f"⚠️ Error opening Router Admin page: {e}",16711680)
    driver.save_screenshot("Airtel-1-error_login_page.png")
    driver.quit()
    raise

# Login to the router
try:
    username = os.getenv('AIRTEL_ROUTER_USERNAME')
    password = os.getenv('AIRTEL_ROUTER_PASSWORD')

    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Frm_Username"))
    )
    password_field = driver.find_element(By.NAME, "Frm_Password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "LoginId"))
    )
    login_button.click()

    driver.save_screenshot("Airtel-2-after_login.png")
    time.sleep(5)  # Wait for login to process
except Exception as e:
    print(f"Error during login: {e}")
    send_discord_notification(f"⚠️ Error during login: {e}",16711680)
    driver.save_screenshot("Airtel-2-error_after_login.png")
    driver.quit()
    raise

# After successful login, wait for and click the Management & Diagnosis link
try:
    mgmt_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "mgrAndDiag"))
    )
    mgmt_link.click()
    
    driver.save_screenshot("Airtel-3-management_page.png")
    time.sleep(5)  # Wait for page to load
except Exception as e:
    print(f"Error clicking Management & Diagnosis link: {e}")
    send_discord_notification(f"⚠️ Error clicking Management & Diagnosis link: {e}",16711680)
    driver.save_screenshot("Airtel-3-error_management_page.png")
    driver.quit()
    raise

# Click on System Management link
try:
    sys_mgmt_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "devMgr"))
    )
    sys_mgmt_link.click()
    
    driver.save_screenshot("Airtel-4-system_management_page.png")
    time.sleep(5)  # Wait for page to load
except Exception as e:
    print(f"Error clicking System Management link: {e}")
    send_discord_notification(f"⚠️ Error clicking System Management link: {e}",16711680)
    driver.save_screenshot("Airtel-4-error_system_management_page.png")
    driver.quit()
    raise

# Click on Reboot button
try:
    reboot_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Btn_restart"))
    )
    reboot_button.click()
    
    driver.save_screenshot("Airtel-5-reboot_confirmation.png")
    time.sleep(5)  # Wait for confirmation dialog

    # Click the OK button in the confirmation dialog
    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "confirmOK"))
    )
    confirm_button.click()
    
    driver.save_screenshot("Airtel-6-reboot_initiated.png")
    time.sleep(5)  # Wait for reboot initiation
except Exception as e:
    print(f"Error during reboot confirmation: {e}")
    send_discord_notification(f"⚠️ Error during reboot confirmation: {e}",16711680)
    driver.save_screenshot("Airtel-6-error_reboot_confirmation.png")
    driver.quit()
    raise

# Clean up
driver.quit()

# Check router online status after reboot
def ping_router(host="10.1.1.1"):
    """
    Returns True if host responds to a ping request
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', host]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

# After reboot is initiated, wait for router to come back online
print("Waiting for router to come back online...")
# send_discord_notification("🔄 Router is rebooting. Waiting for it to come back online...")

router_back = False
attempts = 0
max_attempts = 20  # Maximum 10 minutes (20 attempts × 30 seconds)

while not router_back and attempts < max_attempts:
    time.sleep(30)  # Wait for 30 seconds between pings
    attempts += 1
    
    if ping_router():
        router_back = True
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success_message = f"✅ Router is back online at {current_time} (after {attempts * 30} seconds)"
        print(success_message)
        send_discord_notification(success_message, 65280)
    else:
        print(f"Router still not responding... Attempt {attempts}/{max_attempts}")

if not router_back:
    failure_message = f"❌ Router did not come back online after {max_attempts * 30} seconds"
    print(failure_message)
    send_discord_notification(failure_message)

# Cron job setup
# https://chatgpt.com/share/684ee8fe-13cc-8002-8c5a-93a933462092