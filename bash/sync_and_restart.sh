#!/bin/bash

# Set environment variables explicitly
export HOME=/home/vhpadmin
export USER=vhpadmin
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Load user profile if exists
[ -f "$HOME/.profile" ] && source "$HOME/.profile"
[ -f "$HOME/.bashrc" ] && source "$HOME/.bashrc"

# Set working directory
cd /usr1/vhp-serverless || {
    echo "❌ Failed to change directory to /usr1/vhp-serverless"
    exit 1
}

# Check if virtualenv exists
if [ ! -f "/usr1/vhp-serverless/lenv/bin/activate" ]; then
    echo "❌ Virtual environment not found at /usr1/vhp-serverless/lenv/bin/activate"
    exit 1
fi

# Aktifkan virtualenv
echo "🔧 Activating virtual environment..."
source /usr1/vhp-serverless/lenv/bin/activate || {
    echo "❌ Failed to activate virtual environment"
    exit 1
}

# Check if Python script exists
if [ ! -f "/usr1/vhp-serverless/sync_functions.py" ]; then
    echo "❌ sync_functions.py not found"
    exit 1
fi

# Jalankan script sinkronisasi
echo "🔄 Running synchronization script..."
python /usr1/vhp-serverless/sync_functions.py || {
    echo "❌ Synchronization script failed"
    exit 1
}

# Restart service
echo "🔄 Restarting vhppy service..."
sudo systemctl restart vhppy || {
    echo "❌ Failed to restart vhppy service"
    exit 1
}

echo "✅ All operations completed successfully"