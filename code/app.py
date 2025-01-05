from scheduler import Scheduler
from driver import SheetDriver
from monitor import TaskMonitor, HOST_ADDR, PORT
from proxy_enabler import enableProxyServer, disableProxyServer
from datetime import datetime
import backend
import time
import sys
import json

# Reading configuration details from 'config.json'.
file_path = 'config.json'
try:
    with open(file_path, 'r') as file:
        config = json.load(file)
        print(f"Configuration loaded successfully from {file_path}.")
except FileNotFoundError:
    print(f"Error: Configuration file not found at {file_path}.")
    sys.exit()
except json.JSONDecodeError as e:
    print(f"Error: Failed to decode JSON file. Check the file format. {e}")
    sys.exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit()

# A test function to demonstrate the usage of Scheduler and SheetDriver classes.
def test1():
    # Create a Scheduler instance using the CSV URL.
    test_schedule = Scheduler(config['csv url'])

    # Retrieve a specific day ('12/7/2024') and mark all tasks as completed.
    before = test_schedule['12/7/2024']
    before.setAll()
    test_schedule[before.date] = before  # Update the schedule.

    # Get the checkboxes for the specified day.
    boxes = test_schedule.getCheckboxes('12/7/2024')

    # Initialize the SheetDriver with credentials and interact with the sheet.
    test_driver = SheetDriver(config['credentials path'])
    test_driver.openSheet(config['sheet name'], config['sheet number'])
    test_driver.checkBoxes(boxes)  # Check all boxes.
    test_driver.uncheckBoxes(boxes)  # Uncheck all boxes.

def test2():
    enableProxyServer(HOST_ADDR, PORT)
    tasks = ['Example1', 'Example2', 'Example3']
    backend.launchWebApp(tasks)
    monitor = TaskMonitor()
    monitor.activate()

    while monitor.active:

        tasks_from_web = backend.getTasksFromWebApp()
        all_done = all(task['completed'] for task in tasks_from_web)

        if all_done:
            monitor.deactivate()

    time.sleep(5)
    disableProxyServer()
    print("ALL DONE :)")

def test3():
    run()

def run():
    monitor = TaskMonitor()
    schedule = Scheduler(config['csv url'])
    sheet_driver = SheetDriver(config['credentials path'])
  
    date = datetime.now()
    m, d, y = str(date.month), str(date.day), str(date.year)
    day = date.strftime('%A').lower()
    morning = date.strftime('%p').lower() == 'am'
    date = f'{m}/{d}/{y}'

    if date not in set(schedule.sheet_data['Date']):
        print("Can't find this day.")
        return
 
    today = schedule[date]
    if morning and day not in {'saturday', 'sunday'}:
        today = today.getMorning()
    today.setEmpty()
    if today.isDone():
        return

    tasks = today.getNotDone()

    enableProxyServer(HOST_ADDR, PORT)

    backend.launchWebApp(tasks)

    monitor.activate()

    while monitor.active:

        tasks_from_web = backend.getTasksFromWebApp()
        all_done = all(task['completed'] for task in tasks_from_web)

        if all_done:
            monitor.deactivate()
            time.sleep(5)

    disableProxyServer()

    today.setAll()
    boxes_to_check = schedule.getCheckboxes(date)

    sheet_driver.openSheet(config['sheet name'], config['sheet number'])
    sheet_driver.checkBoxes(boxes_to_check)


# Entry point of the script. Executes the test functions.
if __name__ == '__main__':
    #test1()
    #test2()
    test3()
else:
    run()
