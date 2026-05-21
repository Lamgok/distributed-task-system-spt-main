from aiohttp import web
from multiprocessing import (
    Manager,
    Process,
    Queue,
    freeze_support
)

from queue_manager import next_counter

from worker import worker_loop

import shared_data

task_queue = None

from system_logger import write_log

# ==========================================
# PRIORITY MAP
# ==========================================

priority_map = {

    "HIGH": 1,

    "MEDIUM": 2,

    "LOW": 3
}

# ==========================================
# SUBMIT TASK
# ==========================================

async def submit_task(request):

    data = await request.json()

    task_name = data["task"]

    priority_text = data["priority"]

    priority = priority_map[priority_text]

    task = {

        "name": task_name,

        "retry": 0
    }

    task_queue.put(

        (
            priority,
            next_counter(),
            task
        )
    )

    shared_data.system_data["received"] += 1

    write_log(

        f"Task {task_name} submitted "
        f"with priority {priority_text}"
    )

    return web.json_response({

        "status": "submitted"
    })

# ==========================================
# STATUS API
# ==========================================

async def status(request):

    data = {
        "completed": shared_data.system_data["completed"],
        "failed": shared_data.system_data["failed"],
        "received": shared_data.system_data["received"],
        "processing": list(shared_data.system_data["processing"]),
        "completed_tasks": list(shared_data.system_data["completed_tasks"]),
        "failed_tasks": list(shared_data.system_data["failed_tasks"])
    }

    return web.json_response(data)

# ==========================================
# START SERVER
# ==========================================

def start_server():

    app = web.Application()

    app.router.add_post(
        "/task",
        submit_task
    )

    app.router.add_get(
        "/status",
        status
    )

    write_log(
        "Server started on port 8080"
    )

    web.run_app(
        app,
        port=8080
    )

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    freeze_support()

    manager = Manager()

    shared_data.init_shared_data(manager)

    task_queue = Queue()

    workers = []

    NUMBER_OF_WORKERS = 3

    for i in range(NUMBER_OF_WORKERS):

        p = Process(

            target=worker_loop,

            args=(i + 1, task_queue, shared_data.system_data, shared_data.lock)
        )

        p.start()

        workers.append(p)

    start_server()