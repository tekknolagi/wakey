#!/usr/bin/env python3
import subprocess
print("Content-Type: text/html")
print()

result = subprocess.run(["ping", "-c", "1", "-w", "1", "cedar"], capture_output=True)
if result.returncode == 0:
    print("Awake")
else:
    print("Asleep")
