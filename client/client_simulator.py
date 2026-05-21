import requests
import random
import time

priorities = [

    "HIGH",

    "MEDIUM",

    "LOW"
]

for i in range(15):

    task_name = f"Task-{i}"

    priority = random.choice(
        priorities
    )

    response = requests.post(

        "http://localhost:8080/task",

        json={

            "task": task_name,

            "priority": priority
        }
    )

    print(

        f"{task_name} submitted "
        f"({priority})"
    )

    time.sleep(0.5)