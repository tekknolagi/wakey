#!/usr/bin/env python3
import subprocess
print("Content-Type: text/html")
print()
result = subprocess.run(["wakeonlan", "38:d5:47:e1:e9:15"], capture_output=True)
if result.returncode != 0:
    print("<pre>")
    print("stderr:", result.stderr.decode('utf-8'))
    print("stdout:", result.stdout.decode('utf-8'))
    print("</pre>")
else:
    print("He has risen")
