#!/bin/bash

# Aktifkan virtualenv (jika perlu)
source /usr1/vhp-serverless/lenv/bin/activate

# Jalankan script sinkronisasi
/usr1/vhp-serverless/lenv/bin/python3.11 /usr1/vhp-serverless/sync_functions.py

# Restart service
sudo systemctl restart vhppy

