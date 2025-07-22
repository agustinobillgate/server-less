import paramiko
import time
import os
from dotenv import load_dotenv

load_dotenv()
hostname = os.getenv("SSH_HOST")
port = int(os.getenv("SSH_PORT", 22))
username = os.getenv("SSH_USERNAME")
private_key_path = os.getenv("SSH_KEY_PATH")

# Commands to run
screen_name = 'gunicorn'
gunicorn_cmd = (
    'gunicorn main:app '
    '-k uvicorn.workers.UvicornWorker '
    '--workers 5 '
    '--max-requests 200 '
    '--max-requests-jitter 50 '
    '--timeout 200 '
    '--keep-alive 5'
)

def run_remote_gunicorn():
    key = paramiko.RSAKey.from_private_key_file(private_key_path)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, port=port, username=username, pkey=key)
        shell = client.invoke_shell()
        time.sleep(1)

        # Attach to screen session
        shell.send('screen -r g\n')  # 'g' is your tab completion prefix
        time.sleep(2)

        # Stop existing gunicorn (CTRL+C)
        shell.send('\x03')  # Ctrl-C
        time.sleep(2)

        # Run gunicorn again
        shell.send('cd /usr1/serverless/src\n')
        time.sleep(1)
        shell.send(f'{gunicorn_cmd}\n')
        time.sleep(3)

        # Detach from screen (Ctrl-A d)
        shell.send('\x01d')  # Ctrl-A then d to detach
        time.sleep(1)

        # Optional: confirm output
        output = shell.recv(5000).decode()
        print(output)

    finally:
        client.close()

if __name__ == '__main__':
    run_remote_gunicorn()
