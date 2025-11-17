import logging

import paramiko

# Basic logging setup for this module (can be overridden by main)
logging.getLogger(__name__).setLevel(logging.INFO)

def connect_sftp(hostname, port, username, password):
    """
    Establishes a connection to an SFTP server using password authentication.
    """
    transport = None
    sftp_client = None
    try:
        logging.debug(
            f"Attempting to connect to {hostname}:{port} with user {username}..."
        )
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp_client = paramiko.SFTPClient.from_transport(transport)
        logging.info(f"Successfully connected to SFTP server: {hostname}")
        return sftp_client, None
    except Exception as e:
        if transport:
            transport.close()
        logging.error(f"SFTP connection failed for {hostname}: {e}")
        return None, f"SFTP connection failed: {e}"

        return None, f"SFTP connection failed: {e}"

def disconnect_sftp(sftp_client):
    """
    Closes an SFTP client connection and its underlying transport.
    """
    if sftp_client:
        try:
            sftp_client.close()
            if sftp_client.transport:
                sftp_client.transport.close()
            logging.debug("SFTP client and transport disconnected.")
        except Exception as e:
            logging.warning(f"Error during SFTP client disconnect: {e}")
