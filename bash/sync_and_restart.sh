#!/bin/bash

# Aktifkan virtualenv (jika perlu)
source /usr1/vhp-serverless/lenv/bin/activate

# Jalankan script sinkronisasi
python /usr1/vhp-serverless/sync_functions.py

# Restart service
sudo systemctl restart vhppy

