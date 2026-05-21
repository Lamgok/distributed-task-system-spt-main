from multiprocessing import Manager

# ==========================================
# SHARED STATE
# ==========================================
system_data = None
lock = None

def init_shared_data(manager: Manager):
    global system_data, lock

    lock = manager.Lock()

    # Menggunakan list standard bawaan [] di dalam manager.dict
    # agar sinkronisasi data antarproses berjalan dengan baik
    system_data = manager.dict({
        "completed": 0,
        "failed": 0,
        "received": 0,
        "processing": [],
        "completed_tasks": [],
        "failed_tasks": []
    })