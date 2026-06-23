# SPDX-License-Identifier: GPL-3.0-only

import subprocess
import sys
from pathlib import Path


command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
lines = result.stdout.splitlines()
tail = "\n".join(lines[-160:]) + "\n"
Path("python38-diagnostic.txt").write_text(tail, encoding="utf-8")
print(tail)
raise SystemExit(result.returncode)
