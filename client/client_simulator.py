import requests
import random
import time

# Menambahkan prioritas baru sesuai kebutuhan
priorities = [
    "HIGH",
    "MEDIUM",
    "LOW",
    "TALL",
    "SHORT"
]

for i in range(15):
    task_name = f"Task-{i}"
    priority = random.choice(priorities)

    response = requests.post(
        "http://localhost:8080/task",
        json={
            "task": task_name,
            "priority": priority
        }
    )

    print(f"{task_name} submitted ({priority})")
    time.sleep(0.5)