# =========================================
# Rulita, 05-11-2025
# For testing
# =========================================

from functions.additional_functions import *
import os
from datetime import date

def test_generate_file():

    htl_no: str = "001"
    file_dir: str = "/usr1/serverless/src/additional_files"
    file_path: str = os.path.join(file_dir, "test_output_" + htl_no + ".txt")
    file_message: str = ""
    it_exists: bool = False

    def generate_output():
        nonlocal htl_no, file_dir, file_path, file_message, it_exists
        return {
            "status": "success",
            "file_path": file_path,
        }

    os.makedirs(file_dir, exist_ok=True)

    def generate_files(file_message):
        formatted_message = f"{file_message}\n"
        with open(file_path, "a") as write_message:
            write_message.write(formatted_message)

    file_message = "Test1 ; Test test ;" + "''"
    generate_files(file_message)
    file_message = "Test2 ; Test tested ;"
    generate_files(file_message)
    it_exists = True

    return generate_output()
