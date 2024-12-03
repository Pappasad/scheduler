from scheduler import Scheduler

with open('url.txt', 'r') as input:
    url = input.read()

def test():
    test_schedule = Scheduler(url)
    print(test_schedule['12/2/2024'])




def run():
    pass

if __name__ == '__main__':
    test()
    
        
