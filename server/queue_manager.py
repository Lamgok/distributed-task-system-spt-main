from queue import PriorityQueue
from multiprocessing import Value
from ctypes import c_int

# ==========================================
# PRIORITY QUEUE
# ==========================================

task_queue = PriorityQueue()

# ==========================================
# COUNTER
# ==========================================

task_counter = Value(c_int, 0)

# ==========================================
# NEXT COUNTER
# ==========================================

def next_counter():

    with task_counter.get_lock():

        task_counter.value += 1

        return task_counter.value