import time
import uuid

# ==========================================
# NEXT COUNTER
# ==========================================
def next_counter():
    return (time.time_ns(), uuid.uuid4())