import os
import shutil
import subprocess
from datetime import datetime
import sys

def get_current_commit_hash():
    try:
        result = subprocess.run(['git', 'rev-parse', 'HEAD'],
                                capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def get_current_branch():
    try:
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                                capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def get_git_log_between(start_hash, end_hash):
    try:
        result = subprocess.run(['git', 'log', f'{start_hash}..{end_hash}', '--oneline'],
                                capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "⚠️ Failed to retrieve git log."

def get_git_diff_between(start_hash, end_hash):
    try:
        result = subprocess.run(['git', 'diff', f'{start_hash}..{end_hash}'],
                                capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "⚠️ Failed to retrieve git diff."

def git_reset_hard(log_dir='logs'):
    """Reset the repository to HEAD, discarding all local changes"""
    log_file = os.path.join(log_dir, 'git_pull_history.log')
    
    try:
        result = subprocess.run(['git', 'reset', '--hard', 'HEAD'],
                                capture_output=True, text=True, check=True)
        
        with open(log_file, 'a') as log:
            log.write(f"\n=== Git Reset --hard at {datetime.now().isoformat()} ===\n")
            log.write("Output from `git reset --hard HEAD`:\n")
            log.write(result.stdout + "\n")
            log.write("="*60 + "\n")
        
        print("🔄 Git reset --hard completed successfully.")
        return True
    
    except subprocess.CalledProcessError as e:
        print("❌ Failed to reset git repository:")
        print(e.stderr)
        
        with open(log_file, 'a') as log:
            log.write(f"\n=== Git Reset --hard FAILED at {datetime.now().isoformat()} ===\n")
            log.write("Error:\n")
            log.write(e.stderr)
            log.write("="*60 + "\n")
        
        return False

def git_pull(log_dir='logs'):
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'git_pull_history.log')

    branch = get_current_branch()
    if not branch:
        print("❌ Failed to detect current git branch.")
        return False

    # First, reset --hard to discard local changes
    print("🔄 Resetting repository to discard local changes...")
    if not git_reset_hard(log_dir):
        print("❌ Failed to reset repository. Aborting.")
        return False

    before_hash = get_current_commit_hash()

    try:
        result = subprocess.run(['git', 'pull', 'origin', branch],
                                capture_output=True, text=True, check=True)

        after_hash = get_current_commit_hash()

        commit_changed = before_hash != after_hash
        git_log = get_git_log_between(before_hash, after_hash) if commit_changed else "No new commits."
        git_diff = get_git_diff_between(before_hash, after_hash) if commit_changed else "No changes in code."

        with open(log_file, 'a') as log:
            log.write(f"\n=== Git Pull at {datetime.now().isoformat()} ===\n")
            log.write(f"Branch       : {branch}\n")
            log.write(f"Before Commit: {before_hash}\n")
            log.write(f"After Commit : {after_hash}\n\n")
            log.write("Output from `git pull`:\n")
            log.write(result.stdout + "\n")
            log.write("Git Log (oneline summary):\n")
            log.write(git_log + "\n\n")
            log.write("Git Diff (code changes):\n")
            log.write(git_diff + "\n")
            log.write("="*60 + "\n")

        print(result.stdout)
        return True

    except subprocess.CalledProcessError as e:
        print("❌ Failed to pull from git:")
        print(e.stderr)

        with open(log_file, 'a') as log:
            log.write(f"\n=== Git Pull FAILED at {datetime.now().isoformat()} ===\n")
            log.write(f"Branch: {branch}\n")
            log.write(f"Before Commit: {before_hash}\n")
            log.write("Error:\n")
            log.write(e.stderr)
            log.write("="*60 + "\n")

        return False

def copy_and_log(src_dir, dst_dir, log_file, step_name):
    if not os.path.exists(src_dir):
        print(f"[WARNING] Source directory not found: {src_dir}")
        return

    files_copied = 0
    with open(log_file, 'a') as log:
        log.write(f"\n--- {step_name} STARTED at {datetime.now().isoformat()} ---\n")

        for root, _, files in os.walk(src_dir):
            rel_path = os.path.relpath(root, src_dir)
            dest_root = os.path.join(dst_dir, rel_path) if rel_path != '.' else dst_dir

            os.makedirs(dest_root, exist_ok=True)

            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dest_root, file)

                try:
                    action = "REPLACED" if os.path.exists(dst_file) else "COPIED"
                    shutil.copy2(src_file, dst_file)
                    log_entry = f"{datetime.now().isoformat()} | {action} | {src_file} -> {dst_file}\n"
                    log.write(log_entry)
                    files_copied += 1
                except Exception as e:
                    error_entry = f"{datetime.now().isoformat()} | ERROR | {src_file} -> {dst_file} | {e}\n"
                    log.write(error_entry)

        log.write(f"--- {step_name} COMPLETED: {files_copied} files processed ---\n")

def main():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    os.chdir(BASE_DIR)

    logs_dir = os.path.join(BASE_DIR, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, 'sync_functions_timestamps.log')

    # Step 0: Git Reset --hard + Git Pull (Dynamic Branch)
    if not git_pull(log_dir=logs_dir):
        print("❌ Aborting due to git pull failure.")
        sys.exit(1)

    # Step 1
    print("📁 Step 1: Syncing from converted2 -> functions ...")
    copy_and_log(
        src_dir=os.path.join(BASE_DIR, 'converted2'),
        dst_dir=os.path.join(BASE_DIR, 'functions'),
        log_file=log_file,
        step_name="STEP 1: converted2 -> functions"
    )

    # Step 2
    print("📁 Step 2: Syncing from functions_py -> functions ...")
    copy_and_log(
        src_dir=os.path.join(BASE_DIR, 'functions_py'),
        dst_dir=os.path.join(BASE_DIR, 'functions'),
        log_file=log_file,
        step_name="STEP 2: functions_py -> functions"
    )

    print("✅ All done. Logs written to:")
    print(f"  - {log_file}")
    print(f"  - {os.path.join(logs_dir, 'git_pull_history.log')}")

if __name__ == '__main__':
    main()