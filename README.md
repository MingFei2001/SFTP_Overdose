# SFTP_Overdose

> A Python-based tool to stress test an SFTP server by simulating multiple concurrent download connections and measuring their performance. Ideal for evaluating NAS limits.

## Features

*   Simulates multiple concurrent SFTP downloads.
*   Reports average, min, and max download speeds (MB/s).
*   Tracks successful and failed operations.
*   Configurable SFTP server, file path/size, threads, and duration.
*   Password-based authentication.
*   Automatic cleanup of temporary local files.
*   Basic logging.

## Prerequisites

*   **Python 3.x** (Any modern Python 3.x version is suitable)
*   **SFTP Server** with:
    *   Valid username/password.
    *   An existing large file at a known path, with its size in MB.

## Setup & Installation

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

## Configuration

Before running the script, export the following environment variables:

**Linux/macOS:**
```bash
export SFTP_USERNAME="your_sftp_username"   # Replace with your SFTP username
export SFTP_PASSWORD="your_sftp_password"   # Replace with your SFTP password
```

**Windows (Command Prompt):**
```cmd
set SFTP_USERNAME="your_sftp_username"   REM Replace with your SFTP username
set SFTP_PASSWORD="your_sftp_password"   REM Replace with your SFTP password
```
**Windows (PowerShell):**
```powershell
$env:SFTP_USERNAME="your_sftp_username"   # Replace with your SFTP username
$env:SFTP_PASSWORD="your_sftp_password"   # Replace with your SFTP password
```

Update the variable below in `config.py` to reflect your SFTP server and test parameters.

```SFTP_Overdose/config.py
# --- SFTP Server Configuration ---
SFTP_HOSTNAME = "your_sftp_host"  # REPLACE with hostname/IP
SFTP_PORT = 22                   # REPLACE if non-standard

# --- Test Specific Configuration ---
REMOTE_DOWNLOAD_FILE_PATH = "/path/to/your/large_file.bin" # REPLACE with exact remote file path
REMOTE_FILE_SIZE_MB = 100                                 # REPLACE with ACTUAL file size in MB

# --- Stress Test Parameters ---
NUM_CONCURRENT_THREADS = 20 # Number of simultaneous connections
```
**Ensure all `REPLACE` placeholders are updated and environment variables are set before running.**

## Running the Test

After configuration, execute the main script:

```bash
python SFTP_Overdose/main.py
```
The script will perform an initial connection test, then start multi-threaded downloads with real-time logging.

## Interpreting Results

The script summarizes results after `TEST_DURATION_SECONDS`:

*   **Overall Average Download Speed**: Average speed across all successful operations (MB/s).
*   **Minimum/Maximum Recorded Speed**: Lowest/highest individual speeds (MB/s).
*   **Total Successful/Failed Download Operations**: Counts of operations.

High failures or degraded speeds indicate server/network/storage bottlenecks.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for full details.
