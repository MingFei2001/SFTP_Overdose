import os

# --- SFTP Server Configuration ---
SFTP_HOSTNAME = "10.254.2.40"
SFTP_PORT = 22
SFTP_USERNAME = os.getenv("SFTP_USERNAME")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD")

# --- Test Specific Configuration ---
REMOTE_DOWNLOAD_FILE_PATH = "/test.pdf"
REMOTE_FILE_SIZE_MB = 10.2  # Actual size in MB of the file at REMOTE_DOWNLOAD_FILE_PATH

# --- Stress Test Parameters ---
NUM_CONCURRENT_THREADS = 15


# --- Logging Configuration ---
LOG_FILE_PATH = "sftp_stress_test.log"  # Name of the log file
