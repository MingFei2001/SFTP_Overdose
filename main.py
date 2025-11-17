import logging

from config import (
    NUM_CONCURRENT_THREADS,
    REMOTE_DOWNLOAD_FILE_PATH,
    REMOTE_FILE_SIZE_MB,
    SFTP_HOSTNAME,
    SFTP_PASSWORD,
    SFTP_PORT,
    SFTP_USERNAME,
    TEST_DURATION_SECONDS,
)
from sftp_connector import (  # Imported for validation/initial connection test
    connect_sftp,
    disconnect_sftp,
)
from sftp_tester import SFTPStressTester

# Centralized logging configuration for the main script
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(threadName)s - %(levelname)s - %(message)s",
)


def run_sftp_stress_test():
    """
    Configures and runs the SFTP download stress test.
    """
    # Basic input validation from config.py
    if (
        SFTP_HOSTNAME == "your_sftp_host"
        or SFTP_USERNAME == "your_username"
        or SFTP_PASSWORD == "your_password"
    ):
        logging.error(
            "Please update SFTP_HOSTNAME, SFTP_USERNAME, and SFTP_PASSWORD in SFTP_Overdose/config.py."
        )
        return
    if (
        REMOTE_DOWNLOAD_FILE_PATH == "/path/to/your/large_file.bin"
        or REMOTE_FILE_SIZE_MB == 100
    ):
        logging.error(
            "Please update REMOTE_DOWNLOAD_FILE_PATH and REMOTE_FILE_SIZE_MB in SFTP_Overdose/config.py."
        )
        return

    # Optional: Initial connection test before starting full stress test
    logging.info("Performing initial SFTP connection test...")
    sftp_client, error = connect_sftp(
        SFTP_HOSTNAME, SFTP_PORT, SFTP_USERNAME, SFTP_PASSWORD
    )
    if error:
        logging.critical(f"Initial connection failed. Aborting stress test: {error}")
        return
    else:
        logging.info("Initial SFTP connection successful.")
        disconnect_sftp(sftp_client)  # Close the test connection

    logging.info(
        f"Preparing SFTP download stress test with {NUM_CONCURRENT_THREADS} concurrent threads, "
        f"targeting '{REMOTE_DOWNLOAD_FILE_PATH}' ({REMOTE_FILE_SIZE_MB}MB) for {TEST_DURATION_SECONDS} seconds."
    )

    tester = SFTPStressTester(
        hostname=SFTP_HOSTNAME,
        port=SFTP_PORT,
        username=SFTP_USERNAME,
        password=SFTP_PASSWORD,
        remote_file_path=REMOTE_DOWNLOAD_FILE_PATH,
        remote_file_size_mb=REMOTE_FILE_SIZE_MB,
        num_threads=NUM_CONCURRENT_THREADS,
        test_duration_seconds=TEST_DURATION_SECONDS,
    )
    tester.start_test()

    logging.info("\n--- SFTP Download Stress Test Results Summary ---")
    if tester.download_speeds:
        avg_download = sum(tester.download_speeds) / len(tester.download_speeds)
        logging.info(
            f"Overall Average Download Speed (across all successful operations): {avg_download:.2f} MB/s"
        )
    else:
        logging.info("No successful downloads were recorded.")

    logging.info(
        f"Total Successful Download Operations: {tester.successful_operations}"
    )
    logging.info(f"Total Failed Download Operations: {tester.failed_operations}")


if __name__ == "__main__":
    run_sftp_stress_test()
