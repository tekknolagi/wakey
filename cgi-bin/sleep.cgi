#!/usr/bin/env python3
import subprocess
print("Content-Type: text/html")
print()
# The MAC is reversed because that's how sleep-on-lan works
# The port is 8009 because I did not feel like letting it run on a privileged
# port (9)
result = subprocess.run(["wakeonlan", "15:e9:e1:47:d5:38", "-p", "8009"], capture_output=True)
if result.returncode != 0:
    print("<pre>")
    print("stderr:", result.stderr.decode('utf-8'))
    print("stdout:", result.stdout.decode('utf-8'))
    print("</pre>")
else:
    print("Goodnight sweet prince")
