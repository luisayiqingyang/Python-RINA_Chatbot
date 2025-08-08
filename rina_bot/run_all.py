import subprocess
import threading
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_flask():
    flask_dir = os.path.join(BASE_DIR, "frontend")
    subprocess.run(["python", "app.py"], cwd=flask_dir)


def run_fastapi():
    subprocess.run(["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8080", "--reload"], cwd=BASE_DIR)


flask_thread = threading.Thread(target=run_flask)
fastapi_thread = threading.Thread(target=run_fastapi)

flask_thread.start()
fastapi_thread.start()

flask_thread.join()
fastapi_thread.join()
