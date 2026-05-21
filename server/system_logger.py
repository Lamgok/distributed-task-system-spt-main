from datetime import datetime
import os

# ==========================================
# LOG FILE
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

LOG_FILE = os.path.join(
    BASE_DIR,
    "../logs/system.log"
)

# ==========================================
# WRITE LOG
# ==========================================

def write_log(message):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    log_message = f"[{timestamp}] {message}"

    print(log_message)

    with open(LOG_FILE, "a") as f:

        f.write(log_message + "\n")