import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_info(message):
    """Logs informational messages."""
    logging.info(message)

def log_error(message):
    """Logs error messages."""
    logging.error(message)