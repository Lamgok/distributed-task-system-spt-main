from multiprocessing import Manager

# ==========================================
# SHARED STATE
# ==========================================

system_data = None
lock = None


def init_shared_data(manager: Manager):

    global system_data, lock

    lock = manager.Lock()

    system_data = manager.dict({

        "completed": 0,

        "failed": 0,

        "received": 0,

        "processing": manager.list(),

        "completed_tasks": manager.list(),

        "failed_tasks": manager.list()

    })

