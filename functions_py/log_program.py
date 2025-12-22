import os
from datetime import datetime
import psutil

LOG_DIR = "/usr1/serverless/src/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def write_log(level, message, filename="log.txt"):
    log_file_path = os.path.join(LOG_DIR, filename)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] [{level.upper()}] {message}\n"

    with open(log_file_path, "a") as log_file:
        log_file.write(formatted_message)

def log_usage(stage: str):
    process = psutil.Process(os.getpid())

    mem = process.memory_info().rss / (1024 * 1024)   # MB
    cpu = process.cpu_percent(interval=0.1)           # %
    return f"[{stage}] RAM: {mem:.2f} MB | CPU: {cpu:.1f}%"