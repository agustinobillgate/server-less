from datetime import datetime
from functions.additional_functions import *
import psutil
import sys
import os

LOG_DIR = "/usr1/serverless/src/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def write_log(marker, message, filename="log.txt", info="s"):
    """
    Docstring for write_log
    
    :param marker: marker for log
    :param message: message
    :param filename: log file target
    :param style: 's' for simple and 'f' for full 
    """

    frame = sys._getframe(1)  # caller frame
    caller_file = os.path.basename(frame.f_code.co_filename)
    caller_line = frame.f_lineno
    caller_func = frame.f_code.co_name

    tmp_filename = f"{local_storage.hotelCode}-{filename}"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if info == 'f':
        formatted_message = (
            f"[{timestamp}] "
            f"[{marker.upper()}] "
            f"({caller_file} - {caller_func} - line:{caller_line}) "
            f"{message}\n"
        )
    else:
        formatted_message = (
            f"[{timestamp}] "
            f"[{marker.upper()}] "
            f"{message}\n"
        )
        
    with open(os.path.join(LOG_DIR, tmp_filename), "a") as log_file:
        log_file.write(formatted_message)

def log_usage(stage: str):
    process = psutil.Process(os.getpid())

    mem = process.memory_info().rss / (1024 * 1024)   # MB
    cpu = process.cpu_percent(interval=0.1)           # %
    return f"[{stage}] RAM: {mem:.2f} MB | CPU: {cpu:.1f}%"