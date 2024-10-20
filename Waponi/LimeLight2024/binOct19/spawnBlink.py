#!/usr/bin/python
#

import time
import subprocess
import shutil
import os

#### Definitions

process = subprocess.Popen(['python3', 'fastBlink.py'])
# subprocess.run(['python3', '/home/arducam/bin/fastBlink.py'], capture_output=False, text=False)

print(f"Spawned.")
