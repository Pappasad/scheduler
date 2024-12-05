from scheduler import Scheduler
from driver import SheetDriver

# Path to the JSON credentials required for Google Sheets API access.
CREDENTIALS_PATH = "scheduler-443419-d3a6ff019998.json"

# Reading configuration details from 'url.txt'.
with open('url.txt', 'r') as input:
    csv_url = input.readline().strip()  # URL of the CSV file containing the schedule data.
    sheet_name = input.readline().strip()  # Name of the Google Sheet to interact with.
    current_sheet = int(input.readline().strip())  # Index of the active sheet to be used.

# A test function to demonstrate the usage of Scheduler and SheetDriver classes.
def test1():
    # Create a Scheduler instance using the CSV URL.
    test_schedule = Scheduler(csv_url)

    # Retrieve a specific day ('12/7/2024') and mark all tasks as completed.
    before = test_schedule['12/7/2024']
    before.setAll()
    test_schedule[before.date] = before  # Update the schedule.

    # Get the checkboxes for the specified day.
    boxes = test_schedule.getCheckboxes('12/7/2024')

    # Initialize the SheetDriver with credentials and interact with the sheet.
    test_driver = SheetDriver(CREDENTIALS_PATH)
    test_driver.openSheet(sheet_name, current_sheet)
    test_driver.checkBoxes(boxes)  # Check all boxes.
    test_driver.uncheckBoxes(boxes)  # Uncheck all boxes.



# Placeholder for an update function to be implemented in the future.
# TODO: Define the logic for updating the schedule or sheet.
def update():
    pass

# Placeholder for a run function to be implemented in the future.
# TODO: Define the main execution logic.
def run():
    pass



# Entry point of the script. Executes the test functions.
if __name__ == '__main__':
    test1()
