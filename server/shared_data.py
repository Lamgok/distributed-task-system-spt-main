from multiprocessing import Lock

# ==========================================
# LOCK
# ==========================================

lock = Lock()

# ==========================================
# SYSTEM DATA
# ==========================================

system_data = {

    "completed": 0,

    "failed": 0,

    "received": 0,

    "processing": [],

    "completed_tasks": [],

    "failed_tasks": []
}