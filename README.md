# SFTP_Overdose - SFTP Download Stress Tester

A Python-based tool to stress test an SFTP server by simulating multiple concurrent download connections and measuring their performance. Ideal for evaluating NAS limits.

---

## 1. Features

*   Simulates multiple concurrent SFTP downloads.
*   Reports average, min, and max download speeds (MB/s).
*   Tracks successful and failed operations.
*   Configurable SFTP server, file path/size, threads, and duration.
*   Password-based authentication.
*   Automatic cleanup of temporary local files.
*   Basic logging.

## 2. Prerequisites

*   **Python 3.x** (Any modern Python 3.x version is suitable)
*   **SFTP Server** with:
    *   Valid username/password.
    *   An existing large file at a known path, with its size in MB.

## 3. Setup & Installation

1.  **Navigate** to the project directory:
    ```bash
    cd /home/mingfei/Projects/SFTP_Overdose
    ```
2.  **Create & Activate** a Python virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install** dependencies:
    ```bash
    pip install paramiko
    ```
    (Deactivate with `deactivate` when done.)

## 4. Configuration

Edit `SFTP_Overdose/config.py` with your server and test details.

```SFTP_Overdose/config.py
# --- SFTP Server Configuration ---
SFTP_HOSTNAME = "your_sftp_host"  # REPLACE with hostname/IP
SFTP_PORT = 22                   # REPLACE if non-standard
SFTP_USERNAME = "your_username"  # REPLACE with username
SFTP_PASSWORD = "your_password"  # REPLACE with password

# --- Test Specific Configuration ---
REMOTE_DOWNLOAD_FILE_PATH = "/path/to/your/large_file.bin" # REPLACE with exact remote file path
REMOTE_FILE_SIZE_MB = 100                                 # REPLACE with ACTUAL file size in MB

# --- Stress Test Parameters ---
NUM_CONCURRENT_THREADS = 20 # Number of simultaneous connections
TEST_DURATION_SECONDS = 60  # Duration for worker threads
```
**Ensure all `REPLACE` placeholders are updated before running.**

## 5. Running the Test

After configuration, execute the main script:

```bash
python SFTP_Overdose/main.py
```
The script will perform an initial connection test, then start multi-threaded downloads with real-time logging.

## 6. Interpreting Results

The script summarizes results after `TEST_DURATION_SECONDS`:

*   **Overall Average Download Speed**: Average speed across all successful operations (MB/s).
*   **Minimum/Maximum Recorded Speed**: Lowest/highest individual speeds (MB/s).
*   **Total Successful/Failed Download Operations**: Counts of operations.

High failures or degraded speeds indicate server/network/storage bottlenecks.

## 7. Project Structure

```
SFTP_Overdose/
├── config.py             # Configurable parameters.
├── sftp_connector.py     # SFTP connection/disconnection logic.
├── sftp_tester.py        # SFTPStressTester class for multi-threaded test.
└── main.py               # Main entry point: loads config, runs test, displays results.
```

## 8. License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.
