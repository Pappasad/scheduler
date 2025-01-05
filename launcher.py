import sys
import os
import subprocess

venv_dir = '.venv'

if not os.path.exists(venv_dir):
    subprocess.run(['python', '-m', 'venv', venv_dir], check=True)

venv_exe = os.path.abspath(os.path.join(venv_dir, 'Scripts', 'python.exe'))

if not os.path.exists(os.path.join(venv_dir, 'Scripts', 'mitmdump.exe')):
    subprocess.run([venv_exe, '-m', 'pip', *'install -r requirements.txt'.split()])

cmd = os.path.abspath(os.path.join('code', 'app.py'))
subprocess.run([venv_exe, cmd])