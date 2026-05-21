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

    write_log(
        f"Processing {task_name}"
    )

    time.sleep(random.randint(2, 5))

    if random.random() < 0.3:

        raise Exception(
            "Worker crashed!"
        )

    write_log(
        f"Completed {task_name}"
    )

# ==========================================
# WORKER LOOP
# ==========================================

def worker_loop(worker_id, task_queue, system_data, lock):

    write_log(
        f"Worker-{worker_id} started"
    )

    while True:

        priority, order, task = task_queue.get()

        try:

            with lock:

                system_data["processing"].append(
                    task["name"]
                )

            process_task(task)

            with lock:

                system_data["completed"] += 1

                system_data["completed_tasks"].append(
                    task["name"]
                )

                if task["name"] in system_data["processing"]:

                    system_data["processing"].remove(
                        task["name"]
                    )

        except Exception:

            retry_count = task["retry"]

            write_log(
                f"Worker-{worker_id} failed on "
                f"{task['name']}"
            )

            if retry_count < MAX_RETRY:

                task["retry"] += 1

                write_log(
                    f"Retrying {task['name']}"
                )

                task_queue.put(
                    (
                        priority,
                        next_counter(),
                        task
                    )
                )

            else:

                with lock:

                    system_data["failed"] += 1

                    system_data["failed_tasks"].append(
                        task["name"]
                    )

                write_log(
                    f"{task['name']} permanently failed"
                )

            with lock:

                if task["name"] in system_data["processing"]:

                    system_data["processing"].remove(
                        task["name"]
                    )