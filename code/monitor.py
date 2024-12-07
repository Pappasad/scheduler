import subprocess
import os
import threading
import time

# Get absolute paths for mitmdump and the monitor script
mitm_path = os.path.abspath('.venv/Scripts/mitmdump.exe')
script_path = os.path.abspath('code/monitor-script.py')
MONITOR_COMMAND = [mitm_path, '-s', script_path]

class TaskMonitor:
    def __init__(self, task_list):
        """Initialize the TaskMonitor with a list of tasks."""
        self.task_list = task_list
        self.active = False
        self.bg_monitor = None
        self._output_thread = None

    def activate(self):
        """Start the background monitor."""
        if self.bg_monitor is None:
            self.active = True
            try:
                self.bg_monitor = subprocess.Popen(
                    MONITOR_COMMAND,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=os.environ.copy()
                )
                print(f"[MONITOR] Started subprocess with PID: {self.bg_monitor.pid}")

                # Start a thread to read and print the output asynchronously
                self._output_thread = threading.Thread(target=self._read_output, daemon=True)
                self._output_thread.start()

            except Exception as e:
                print(f"<<<ERROR>>> [MONITOR] Failed to start subprocess: {e}")
                self.active = False

    def deactivate(self):
        """Stop the background monitor."""
        if self.bg_monitor is not None:
            try:
                print(f"[MONITOR] Terminating subprocess with PID: {self.bg_monitor.pid}")
                self.bg_monitor.terminate()
                
                # Wait for the process to exit
                self.bg_monitor.wait(timeout=10)
                print(f"[MONITOR] Subprocess with PID {self.bg_monitor.pid} has exited.")
                
            except subprocess.TimeoutExpired:
                print(f"<WARNING> [MONITOR] Subprocess did not exit, killing it...")
                self.bg_monitor.kill()
            
            except Exception as e:
                print(f"<<<ERROR>>> [MONITOR] Error while terminating the subprocess: {e}")
            
            finally:
                self.bg_monitor = None
                self.active = False

    def _read_output(self):
        """Read stdout and stderr of the subprocess and print it."""
        if self.bg_monitor.stdout:
            for line in iter(self.bg_monitor.stdout.readline, b''):
                if line:
                    print(f"\t\t[MONITOR] {line.decode('utf-8').strip()}")

    def __enter__(self):
        """Context manager start method."""
        self.activate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit method."""
        self.deactivate()


if __name__ == '__main__':
    test_monitor = TaskMonitor(['Example'])
    test_monitor.activate()
    time.sleep(20)
    test_monitor.deactivate()