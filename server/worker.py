import time
import random

from queue_manager import next_counter
from system_logger import write_log

MAX_RETRY = 3

# ==========================================
# PROCESS TASK
# ==========================================
def process_task(task):
    task_name = task["name"]
    write_log(f"Processing {task_name}")

    time.sleep(random.randint(2, 5))

    if random.random() < 0.3:
        raise Exception("Worker crashed!")

    write_log(f"Completed {task_name}")

# ==========================================
# WORKER LOOP
# ==========================================
def worker_loop(worker_id, task_queue, system_data, lock):
    write_log(f"Worker-{worker_id} started")

    while True:
        priority, order, task = task_queue.get()

        try:
            with lock:
                # Salin list, tambahkan data, dan masukkan kembali ke shared dict
                current_processing = list(system_data["processing"])
                current_processing.append(task["name"])
                system_data["processing"] = current_processing

            process_task(task)

            with lock:
                system_data["completed"] += 1
                
                current_completed = list(system_data["completed_tasks"])
                current_completed.append(task["name"])
                system_data["completed_tasks"] = current_completed

                current_processing = list(system_data["processing"])
                if task["name"] in current_processing:
                    current_processing.remove(task["name"])
                system_data["processing"] = current_processing

        except Exception:
            retry_count = task["retry"]
            write_log(f"Worker-{worker_id} failed on {task['name']}")

            if retry_count < MAX_RETRY:
                task["retry"] += 1
                write_log(f"Retrying {task['name']}")
                task_queue.put((priority, next_counter(), task))
            else:
                with lock:
                    system_data["failed"] += 1
                    
                    current_failed = list(system_data["failed_tasks"])
                    current_failed.append(task["name"])
                    system_data["failed_tasks"] = current_failed

                write_log(f"{task['name']} permanently failed")

            with lock:
                current_processing = list(system_data["processing"])
                if task["name"] in current_processing:
                    current_processing.remove(task["name"])
                system_data["processing"] = current_processing