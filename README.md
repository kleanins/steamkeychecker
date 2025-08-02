# Steam CD-Key Checker Bot
────────────────────────────────────────────────────────────────────────
Version: 1.0

## Description

Reads "sent.csv" from the user's Desktop, queries each key on the 
Steam Partner "Query CD Key" page, and saves the results to 
"sent_controlled_*.csv" on the Desktop.

---

## Method 1: Easy Usage (.exe)

This is the recommended method for most users.

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

This method is for developers who want to run the Python script directly.

#### Setup & Usage:

1.  Ensure Python and Google Chrome are installed.
2.  Clone this repository or download the source code (`steamkeychecker.py`) to your Desktop.
3.  Open PowerShell or CMD and install the required libraries:
    ```
    pip install pandas selenium webdriver-manager
    ```
    *If that fails, try:*
    ```
    py -m pip install pandas selenium webdriver-manager
    ```
4.  Place your CSV file named "sent.csv" on your Desktop.
5.  The file MUST have a column named "CD Key".
6.  To run the script, first navigate to your Desktop folder in PowerShell/CMD.
    *   *Standard command:*
        ```
        cd Desktop
        ```
    *   *For OneDrive users (PowerShell):*
        ```
        cd "$Env:OneDrive\Desktop"
        ```
    *   *For OneDrive users (CMD):*
        ```
        cd %OneDrive%\Desktop
        ```
7.  Once you are in the Desktop folder, run the script:
    ```
    python steamkeychecker.py
    ```
    *If that fails, try:*
    ```
    py steamkeychecker.py
    ```
8.  A Chrome window will open. Log in to your Steam Partner account.
9.  Follow the prompts in the console to start the process.