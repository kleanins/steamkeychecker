r"""
Steam CD-Key Checker Bot
────────────────────────────────────────────────────────────────────────
Version: 1.1

Description:
Reads 'sent.csv' from the user's Desktop, queries each key on the 
Steam Partner "Query CD Key" page, and saves the results to 
'sent_controlled_*.csv' on the Desktop.

Setup & Usage:
1. Ensure Python and Google Chrome are installed.
2. Open PowerShell and run: 
   pip install pandas selenium webdriver-manager
   
   If that fails
   py -m pip install pandas selenium webdriver-manager
   
3. Place your CSV file named 'sent.csv' on your Desktop.
4. The file MUST have a column named 'CD Key'.
5. Ensure that cdkeycontrol.py is on your Desktop. You can either download the ZIP from the GitHub Gist (click Download ZIP, then extract it to the Desktop), or copy the script’s code and paste it into a new .py file you create on the Desktop.
6. You can try running the .py file with a double-click. If that doesn’t work, follow the steps below to guarantee it runs.
7. To run the script via PowerShell, open PowerShell and type the following commands.
   
   First, you must navigate to your Desktop folder.
   Try the standard command:
   cd Desktop

   If that fails (common for OneDrive users), use this smart command:
   cd "$Env:OneDrive\Desktop"
   or
   cd %OneDrive%\Desktop

   If, in a rare case, neither of the above works, you must use the 
   full, absolute path as a last resort. Example:
   cd "C:\Users\YOUR_USERNAME\OneDrive\Desktop"

   Once you are successfully in the Desktop folder, run the script:
   python cdkeycontrol.py
   
   If that fails
   py cdkeycontrol.py

8. A Chrome window will open. Log in to your Steam Partner account.
9. Follow the prompts in the console to start the process.
"""

import sys
import time
import logging
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# ───────────────────────────────────────────────────────────────
# 1. GLOBAL SETTINGS & UTILITIES
# ───────────────────────────────────────────────────────────────

# Minimize noisy Selenium/urllib3 output
logging.basicConfig(level=logging.WARNING)
LOGGER.setLevel(logging.WARNING)

def get_desktop_path() -> Path:
    """Return the Desktop folder path if it exists; otherwise, use the current directory."""
    desktop = Path(Path.home()) / "Desktop"
    return desktop if desktop.exists() else Path(Path.cwd())

DESKTOP_PATH = get_desktop_path()

def is_logged_in(driver: webdriver.Chrome) -> bool:
    """
    Check if the user is logged in by looking for a specific navigation element
    (the one with 'Dashboard', 'Tools', etc.) which only appears after login.
    This is much more reliable than checking the URL.
    """
    try:
        # Look for the main navigation bar container. If it exists, we are logged in.
        driver.find_element(By.CLASS_NAME, "partner_nav_content")
        return True
    except NoSuchElementException:
        # If the element is not found, we are not logged in.
        return False
    except Exception:
        # For any other unexpected errors, assume not logged in.
        return False

def wait_for_manual_login(driver: webdriver.Chrome) -> None:
    """Pause execution until the user finishes manual sign-in."""
    print("\n[ACTION REQUIRED]")
    print("The script has detected you are not logged in.")
    print("Please sign in to your Steam Partner account in the browser window.")
    input("Once you are logged in, press Enter here to continue…")
    time.sleep(1) # Allow ample time for the page to refresh and load post-login

def safe_get_text(driver: webdriver.Chrome, xpath: str) -> str:
    """Safely return an element's text. Returns an empty string if not found."""
    try:
        return driver.find_element(By.XPATH, xpath).text.strip()
    except Exception:
        return ''

# ───────────────────────────────────────────────────────────────
# 2. CORE FUNCTION
# ───────────────────────────────────────────────────────────────

def check_keys_and_save(driver: webdriver.Chrome, csv_path: Path) -> None:
    """Read keys from a CSV, query their statuses, and save results to a new file."""
    print(f"\n> Reading input file: {csv_path}")
    try:
        # Ensure CD Keys are read as strings to preserve formatting (e.g., leading zeros)
        df = pd.read_csv(csv_path, dtype={'CD Key': str})
    except FileNotFoundError:
        print(f"  [ERROR] File not found. Please ensure '{csv_path.name}' is on your Desktop.")
        return
    except Exception as exc:
        print(f"  [ERROR] Could not read the CSV file. It might be open, corrupted, or formatted incorrectly.")
        print(f"  Details: {exc}")
        return

    if 'CD Key' not in df.columns:
        print("  [ERROR] The input file is missing the required 'CD Key' column. Aborting.")
        return

    # Ensure output columns exist, creating them if they don't
    for col in ['Status', 'Time Activated', 'Package', 'Tag']:
        if col not in df.columns:
            df[col] = ''

    total = len(df)
    activated_count = df[df['Status'].str.strip() == 'Activated'].shape[0]
    processed_count = 0

    print(f"> Found {total} keys to process. Starting...")
    
    for idx, row in df.iterrows():
        processed_count += 1
        
        # Skip keys that have already been confirmed as 'Activated' in a previous run
        if str(row.get('Status', '')).strip() == 'Activated':
            print(f"  [{processed_count}/{total}] Skipping already activated key: {row.get('CD Key', 'N/A')}")
            continue

        cd_key = str(row.get('CD Key', '')).strip()
        if not cd_key:
            print(f"  [{processed_count}/{total}] Skipping empty CD Key entry at row {idx+2}.")
            continue
            
        url = f"https://partner.steamgames.com/querycdkey/cdkey?l=english&cdkey={cd_key}&method=Query"

        # Retry mechanism for transient network errors
        for attempt in range(1, 6):
            try:
                driver.get(url)
                time.sleep(0.5) 
                if "Bad Gateway" not in driver.title and "Bad Gateway" not in driver.page_source:
                    break
                print(f"  [{processed_count}/{total}] Key {cd_key}: Received 502 Bad Gateway. Retrying ({attempt}/5)...")
                time.sleep(2)
            except TimeoutException:
                print(f"  [{processed_count}/{total}] Page timed out for key {cd_key}. Retrying ({attempt}/5)...")
                time.sleep(5)
        else:
            print(f"  [ERROR] Failed to fetch data for key {cd_key} after 5 retries. Skipping.")
            df.at[idx, 'Status'] = 'Network Error'
            continue
            
        # Extract data from the results table
        status = safe_get_text(driver, '/html/body/div[3]/table[1]/tbody/tr[2]/td[1]/span')
        time_activated = safe_get_text(driver, '/html/body/div[3]/table[1]/tbody/tr[2]/td[2]')
        package = safe_get_text(driver, '/html/body/div[3]/table[1]/tbody/tr[2]/td[3]/a')
        tag = safe_get_text(driver, '/html/body/div[3]/table[1]/tbody/tr[2]/td[4]')

        # Update the DataFrame
        df.at[idx, 'Status'] = status
        df.at[idx, 'Time Activated'] = time_activated
        df.at[idx, 'Package'] = package
        df.at[idx, 'Tag'] = tag

        if status == 'Activated':
            activated_count += 1

        status_display = status if status else '(Not Found / Invalid)'
        print(f"  [{processed_count}/{total}] {cd_key} -> {status_display} | Activated: {activated_count}")

    # Save results to a new file, avoiding overwrites
    out_path_base = DESKTOP_PATH / "sent_controlled"
    out_path = DESKTOP_PATH / "sent_controlled.csv"
    counter = 1
    while out_path.exists():
        out_path = out_path_base.with_name(f"{out_path_base.name}_{counter}.csv")
        counter += 1

    try:
        df.to_csv(out_path, index=False, encoding='utf-8-sig')
        print(f"\n[SUCCESS] All keys processed. Results saved to: {out_path}\n")
    except Exception as exc:
        print(f"\n[ERROR] Failed to save the output file. Please check permissions.")
        print(f"  Details: {exc}")

# ───────────────────────────────────────────────────────────────
# 3. SCRIPT ENTRY POINT
# ───────────────────────────────────────────────────────────────

def main() -> None:
    """Prepare Selenium, ensure login, and run the main processing loop."""
    driver = None
    try:
        print("Initializing Steam CD-Key Checker Bot...")
        
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_opts.add_experimental_option("useAutomationExtension", False)
        chrome_opts.add_argument("--log-level=3")
        # The line to disable images has been removed, so they will now load by default.

        try:
            print("> Checking for required Chrome Driver...")
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_opts)

        except WebDriverException as exc:
            print("\n" + "="*60)
            print("[FATAL ERROR] Could not start the Chrome browser.")
            print("Please install or update Google Chrome to the latest version.")
            print(f"Details: {exc}")
            print("="*60)
            sys.exit(1)

        print("> Browser started successfully.")
        
        try:
            # Go to the English version of the site as requested
            driver.get("https://partner.steamgames.com/?l=english")
        except WebDriverException:
            print("\n[ERROR] Failed to connect to Steam. Please check your internet connection.")
            sys.exit(1)

        # Check if login is needed. If so, wait for manual login without further checks.
        if not is_logged_in(driver):
            wait_for_manual_login(driver)
        else:
            print("> Already logged in to Steam Partner.")

        # Interactive command loop
        while True:
            cmd = input("Type 'start' to begin checking keys, or 'quit' to exit: ").strip().lower()
            if cmd == 'quit':
                break
            if cmd != 'start':
                print("  Invalid command. Please try again.")
                continue

            csv_file = DESKTOP_PATH / "sent.csv"
            if not csv_file.exists():
                print(f"  [ERROR] Input file not found at: {csv_file}")
                print("  Please make sure 'sent.csv' is on your Desktop and try again.")
                continue

            check_keys_and_save(driver, csv_file)

    except KeyboardInterrupt:
        print("\n\n> Process interrupted by user. Shutting down.")
    except Exception as exc:
        print(f"\n[UNEXPECTED ERROR] An unknown error occurred: {exc}")
    finally:
        if driver:
            driver.quit()
        print("> Program finished. Browser has been closed.")

if __name__ == "__main__":
    main()