from scheduler import Scheduler
from driver import SheetDriver
from monitor import TaskMonitor, HOST_ADDR, PORT
from proxy_enabler import enableProxyServer, disableProxyServer
from datetime import datetime
import backend
from threading import Thread
import time

# Reading configuration details from 'config.txt'.
with open('config.txt', 'r') as input:
    Csv_Url = input.readline().strip()  # URL of the CSV file containing the schedule data.
    Sheet_Name = input.readline().strip()  # Name of the Google Sheet to interact with.
    Current_Sheet = int(input.readline().strip())  # Index of the active sheet to be used.
    Credentials_Path = input.readline().strip()

# A test function to demonstrate the usage of Scheduler and SheetDriver classes.
def test1():
    # Create a Scheduler instance using the CSV URL.
    test_schedule = Scheduler(Csv_Url)

    # Retrieve a specific day ('12/7/2024') and mark all tasks as completed.
    before = test_schedule['12/7/2024']
    before.setAll()
    test_schedule[before.date] = before  # Update the schedule.

    # Get the checkboxes for the specified day.
    boxes = test_schedule.getCheckboxes('12/7/2024')

    # Initialize the SheetDriver with credentials and interact with the sheet.
    test_driver = SheetDriver(Credentials_Path)
    test_driver.openSheet(Sheet_Name, Current_Sheet)
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
    schedule = Scheduler(Csv_Url)
    sheet_driver = SheetDriver(Credentials_Path)
  
    date = datetime.now()
    m, d, y = str(date.month), str(date.day), str(date.year)
    date = f'{m}/{d}/{y}'
    today = schedule[date]

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

    sheet_driver.openSheet(Sheet_Name, Current_Sheet)
    sheet_driver.checkBoxes(boxes_to_check)


# Entry point of the script. Executes the test functions.
if __name__ == '__main__':
    #test1()
    #test2()
    test3()
else:
    run()
