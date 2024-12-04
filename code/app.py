from scheduler import Scheduler
from driver import Driver
import os


with open('url.txt', 'r') as input:
    csv_url = input.readline().strip()
    driver_url = input.readline().strip()
    profile_path = input.readline().strip()

def test():
    test_schedule = Scheduler(csv_url)
    before = test_schedule['12/7/2024']
    before.setAll(True)
    test_schedule[before.date] = before
    boxes = test_schedule.getCheckboxes('12/7/2024')
    print(boxes)
    test_driver = Driver(profile_path)
    test_driver.openSchedulerOnline(driver_url)
    test_driver.checkBoxes(boxes)
    #print(driver_url)
    #test_driver.openSchedulerOnline(driver_url)


def update():
    pass
    




def run():
    pass

if __name__ == '__main__':
    test()
    
        
