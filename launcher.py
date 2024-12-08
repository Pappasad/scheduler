import subprocess
import os

env = os.path.abspath('.venv/Scripts/python.exe')
app = os.path.abspath('code/app.py')

subprocess.run([env, app])


