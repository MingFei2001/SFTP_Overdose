# --- SFTP Server Configuration ---
SFTP_HOSTNAME = "your_sftp_host"
SFTP_PORT = 22
SFTP_USERNAME = "your_username"
SFTP_PASSWORD = "your_password"

# --- Test Specific Configuration ---
REMOTE_DOWNLOAD_FILE_PATH = "/path/to/your/large_file.bin"
REMOTE_FILE_SIZE_MB = 100  # Actual size in MB of the file at REMOTE_DOWNLOAD_FILE_PATH

# --- Stress Test Parameters ---
NUM_CONCURRENT_THREADS = 20
TEST_DURATION_SECONDS = 60
