import logging
import os
import tempfile
import threading
import time

from sftp_connector import connect_sftp, disconnect_sftp

# Basic logging setup for this module (can be overridden by main)
logging.getLogger(__name__).setLevel(logging.INFO)


class SFTPStressTester:
    def __init__(
        self,
        hostname,
        port,
        username,
        password,
        remote_file_path,
        remote_file_size_mb,
        num_threads=1,
        test_duration_seconds=60,
    ):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.remote_file_path = remote_file_path
        self.remote_file_size_mb = remote_file_size_mb
        self.num_threads = num_threads
        self.test_duration_seconds = test_duration_seconds
        self.stop_event = threading.Event()
        self.successful_operations = 0
        self.failed_operations = 0
        self.download_speeds = []
        self.lock = threading.Lock()

    def _worker(self, thread_id):
        """
        Worker thread logic to perform SFTP download, measure speed, and clean up.
        Each worker continuously connects, downloads, measures, and disconnects
        for the duration of the test.
        """
        thread_name = f"Worker-{thread_id}"
        threading.current_thread().name = thread_name
        logging.info(f"{thread_name} starting...")

        # Generate a unique temporary local filename in the system's temp directory
        # to avoid conflicts between threads or successive downloads by the same thread.
        # This file will be automatically deleted when closed.
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, prefix=f"sftp_download_{thread_id}_", suffix=".tmp"
        )
        local_download_file = temp_file.name
        temp_file.close()  # Close the file handle immediately, it will be opened again by sftp.get

        start_test_time_for_thread = time.time()
        while (
            not self.stop_event.is_set()
            and (time.time() - start_test_time_for_thread) < self.test_duration_seconds
        ):
            sftp = None
            try:
                # 1. Establish SFTP connection
                sftp, error = connect_sftp(
                    self.hostname, self.port, self.username, self.password
                )
                if error:
                    # If connection fails, log error and increment failed counter
                    raise Exception(error)  # Propagate error to the catch block

                logging.info(
                    f"{thread_name} connected to SFTP server and ready to download."
                )

                # 2. Perform Download and Measure Speed
                logging.debug(
                    f"{thread_name} attempting to download {self.remote_file_path} "
                    f"({self.remote_file_size_mb}MB) to {local_download_file}..."
                )
                download_start_time = time.time()
                sftp.get(self.remote_file_path, local_download_file)
                download_end_time = time.time()
                download_duration = download_end_time - download_start_time

                # Calculate speed, avoid division by zero
                download_speed_mbps = (
                    (self.remote_file_size_mb / download_duration)
                    if download_duration > 0
                    else 0
                )

                # 3. Update shared metrics (thread-safe)
                with self.lock:
                    self.download_speeds.append(download_speed_mbps)
                    self.successful_operations += 1

                logging.info(
                    f"{thread_name} successfully downloaded {self.remote_file_path} "
                    f"at {download_speed_mbps:.2f} MB/s."
                )

            except Exception as e:
                logging.error(
                    f"{thread_name} encountered an error during operation: {e}"
                )
                with self.lock:
                    self.failed_operations += 1
            finally:
                # 4. Disconnect SFTP client
                disconnect_sftp(sftp)
                logging.debug(f"{thread_name} disconnected from SFTP server.")

                # 5. Clean up local downloaded file
                if os.path.exists(local_download_file):
                    os.remove(local_download_file)
                    logging.debug(
                        f"Cleaned up local temporary file: {local_download_file}"
                    )

                # Small delay to prevent hammering the server too aggressively in a tight loop
                # This also allows other threads to get CPU time.
                time.sleep(1)

        logging.info(f"{thread_name} finished its test duration.")

    def start_test(self):
        """
        Orchestrates the multi-threaded SFTP download stress test.
        """
        logging.info(
            f"Starting SFTP stress test with {self.num_threads} threads for {self.test_duration_seconds} seconds. "
            f"Target file: {self.remote_file_path} ({self.remote_file_size_mb}MB)."
        )

        threads = []
        for i in range(self.num_threads):
            thread = threading.Thread(
                target=self._worker, args=(i,), name=f"SFTP-Worker-{i}"
            )
            threads.append(thread)
            thread.start()

        # Wait for the main test duration to elapse
        time.sleep(self.test_duration_seconds)

        # Signal all worker threads to stop their loops
        self.stop_event.set()

        # Wait for all worker threads to complete their current operations and exit
        for thread in threads:
            thread.join()

        logging.info("SFTP stress test completed.")
        logging.info(
            f"Total Successful Download Operations: {self.successful_operations}"
        )
        logging.info(f"Total Failed Download Operations: {self.failed_operations}")

        if self.download_speeds:
            avg_download_speed = sum(self.download_speeds) / len(self.download_speeds)
            min_download_speed = min(self.download_speeds)
            max_download_speed = max(self.download_speeds)

            logging.info(f"--- Download Speed Statistics ---")
            logging.info(f"  Overall Average Speed: {avg_download_speed:.2f} MB/s")
            logging.info(f"  Minimum Recorded Speed: {min_download_speed:.2f} MB/s")
            logging.info(f"  Maximum Recorded Speed: {max_download_speed:.2f} MB/s")
            # Optionally, log all individual speeds for detailed analysis
            # logging.debug(f"  All Recorded Speeds (MB/s): {[f'{s:.2f}' for s in self.download_speeds]}")
        else:
            logging.info(
                "No successful downloads were recorded to calculate statistics."
            )
