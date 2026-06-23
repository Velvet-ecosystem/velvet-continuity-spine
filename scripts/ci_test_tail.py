# SPDX-License-Identifier: GPL-3.0-only

import subprocess
import sys


command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
lines = result.stdout.splitlines()
for line in lines[-120:]:
    print(line)
raise SystemExit(result.returncode)
