#!/bin/bash

cd /usr1/serverless/
source ./venv/bin/activate
gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 5 --max-requests 200 --max-requests-jitter 50 --timeout 200 --keep-alive 5
