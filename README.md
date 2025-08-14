# Steam CD-Key Checker Bot
────────────────────────────────────────────────────────────────────────
Version: 1.1

## Description

Reads "sent.csv" from the user's Desktop, queries each key on the 
Steam Partner "Query CD Key" page, and saves the results to 
"sent_controlled_*.csv" on the Desktop.

---

## Method 1: Easy Usage (.exe)

**For Windows users only.** This is the recommended method.

1.  Ensure **Google Chrome** is installed on your computer.
2.  Go to the **[Releases Page](https://github.com/kleanins/steamkeychecker/releases)**.
3.  Download the `SteamKeyChecker.exe` file from the latest release.
4.  Place your `sent.csv` file on your Desktop.
5.  The `sent.csv` file MUST have a column named "CD Key".
6.  Double-click `SteamKeyChecker.exe` to run. A Chrome window will open.
7.  Log in to your Steam Partner account the first time you run it.
8.  Follow the prompts in the console to start the process.

---

## Method 2: Running from Source (.py)

This method is for **Windows, macOS, and Linux** users who want to run the Python script directly.

#### Setup & Usage:

1.  Ensure Python 3 and Google Chrome are installed.
2.  Download the source code (`steamkeychecker.py`) to your Desktop.
3.  Open your **Terminal**.
    
    *   **On macOS, first run this one-time command to install developer tools (if not already installed):**
        ```
        xcode-select --install
        ```
        *(Click "Install" when a window pops up and wait for it to finish.)*

4.  Install the required libraries in the Terminal:
    
    *   **On Windows:**
        ```
        pip install pandas selenium webdriver-manager
        ```
        *If that fails, try:* `py -m pip install ...`

    *   **On macOS or Linux:**
        ```
        pip3 install pandas selenium webdriver-manager
        ```

4.  Place your CSV file named "sent.csv" on your Desktop.
5.  The file MUST have a column named "CD Key".
6.  Navigate to your Desktop folder in your Terminal:

    *   **On Windows (CMD):**
        *   *Standard:* `cd Desktop`
        *   *OneDrive:* `cd %OneDrive%\Desktop`

    *   **On Windows (PowerShell):**
        *   *Standard:* `cd Desktop`
        *   *OneDrive:* `cd "$Env:OneDrive\Desktop"`

    *   **On macOS or Linux:**
        ```
        cd ~/Desktop
        ```
7.  Once in the Desktop folder, run the script:

    *   **On Windows:**
        ```
        python steamkeychecker.py
        ```
        *If that fails, try:*
        ```
        py steamkeychecker.py
        ```

    *   **On macOS or Linux:**
        ```
        python3 steamkeychecker.py
        ```
8.  A Chrome window will open. Log in to your Steam Partner account.
9.  Follow the prompts in the console to start the process.