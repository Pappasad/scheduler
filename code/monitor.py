import subprocess
import os

MONITOR_COMMAND = ['mitmproxy', '-s', 'code/monitor-script.py']

class TaskMonitor:

    def __init__(self, task_list):
        self.task_list = task_list
        self.active = False
        self.bg_monitor = None

    def activate(self):
        if self.bg_monitor is None:
            self.active = True
            
            self.bg_monitor = subprocess.Popen(
                MONITOR_COMMAND,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=os.environ.copy()
            )

            for line in self.bg_monitor.stdout:
                print(line.decode("utf-8"), end="")

    def deactivate(self):
        self.bg_monitor.terminate()
        self.bg_monitor = None
        self.active = False

            
if __name__ == '__main__':
    subprocess.run('"C:/Users/pappasad/OneDrive - Rose-Hulman Institute of Technology/Documents/Python Scripts/scheduler/.venv/Scripts/mitmdump.exe" -s "C:/Users/pappasad/OneDrive - Rose-Hulman Institute of Technology/Documents/Python Scripts/scheduler/code/monitor-script.py"', shell=True)


