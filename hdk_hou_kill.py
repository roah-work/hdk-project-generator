import os
import sys
import psutil
import argparse

parser = argparse.ArgumentParser(description="Kill Houdini instance associated with .hiplc file")
parser.add_argument("-file", required=True, help="Path to the .hiplc file")
args = parser.parse_args()

hiplc_path = os.path.abspath(args.file)
if not os.path.isfile(hiplc_path):
    print(f"ERROR: .hiplc file not found at: {hiplc_path}")
    sys.exit(-1)

# Derive project_dir from hiplc_path
project_dir = os.path.dirname(os.path.abspath(hiplc_path))  # Houdini_<name> folder
temp_dir = os.path.join(project_dir, "temp")
os.makedirs(temp_dir, exist_ok=True)

hiplc_name = os.path.splitext(os.path.basename(hiplc_path))[0].lower()
pid_file = os.path.join(temp_dir, f"SOP_{hiplc_name}.pid")

if not os.path.exists(pid_file):
    print("No previous Houdini PID found. Skipping kill.")
    sys.exit(0)

try:
    with open(pid_file, "r") as f:
        pid = int(f.read().strip())

    proc = psutil.Process(pid)
    if proc.name().lower() == "houdini.exe":
        print(f"Killing previous Houdini instance (PID {pid})...")
        proc.terminate()
        proc.wait(timeout=5)
    else:
        print(f"PID {pid} is not Houdini. Skipping.")
except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError) as e:
    print(f"Failed to validate or kill previous process: {e}")
