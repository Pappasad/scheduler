import subprocess
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

env = os.path.abspath('.venv/Scripts/python.exe')
app = os.path.abspath('code/app.py')

subprocess.run([env, app])


