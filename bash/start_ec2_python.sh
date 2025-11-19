#!/bin/bash

# 1. Rename file A to B (overwrite if exists)
cd /usr1/serverless/
# mv -f /usr1/serverless/src/functions/additional_functions_ori.py /usr1/serverless/src/functions/additional_functions.py

# 2. Start the virtual environment
source ./venv/bin/activate

# 3. Run the application using PyPy3 and Uvicorn
uvicorn main:app --host 0.0.0.0 --workers 5
