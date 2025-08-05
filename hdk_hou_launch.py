import os
import subprocess
import time
import sys
import psutil
import argparse

parser = argparse.ArgumentParser(description="Launch Houdini with specified .hiplc file")
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

# Resolve houdini.exe from HFS
houdini_exe = os.path.join(os.environ.get("HFS", ""), "bin", "houdini.exe")
if not os.path.exists(houdini_exe):
    print("ERROR: houdini.exe not found from HFS.")
    sys.exit(-1)

# Launch Houdini
print(f"Launching Houdini from: {houdini_exe}")
print(f"Opening file: {hiplc_path}")
proc = subprocess.Popen([houdini_exe, hiplc_path])

# Write PID
hiplc_name = os.path.splitext(os.path.basename(hiplc_path))[0].lower()
pid_file = os.path.join(temp_dir, f"SOP_{hiplc_name}.pid")
with open(pid_file, "w") as f:
    f.write(str(proc.pid))

print(f"Houdini launched (PID {proc.pid})")
