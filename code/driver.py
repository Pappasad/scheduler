from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Driver(webdriver.Firefox):

    def __init__(self, profile):
        self.open_sheet = False
        self.options = Options()
        self.options.add_argument(f'--profile {profile}')
        super().__init__(options=self.options)

    def openSchedulerOnline(self, url):
        self.get(url)
        self.open_sheet = True
        time.sleep(5)

    def checkBoxes(self, boxes):
        if not self.open_sheet:
            print("SHEET NOT OPEN AAAAAH")
            return
        
        for row, col in boxes:
            cell_xpath = f'//div[@aria-colindex="{col}" and @aria-rowindex="{row}"]'
            wait = WebDriverWait(self, 10)
            try:
                # Find the cell and click it
                checkbox_cell = wait.until(EC.presence_of_element_located((By.XPATH, cell_xpath)))
                checkbox_cell.click()
                time.sleep(0.5)  # Allow time for the click to register
            except Exception as e:
                print(f"Failed to update checkbox at row {row}, column {col}: {e}")

        time.sleep(2)

    def quit(self):
        super()
        self.open_sheet = False


    def googleLogin(self, email, password):
        pass
        # self.get("https://accounts.google.com/signin")
        # email_field = self.find_element(By.ID, "identifierId")
        # email_field.send_keys(email)
        # email_field.send_keys(Keys.ENTER)
        # time.sleep(3)
        # password_field = self.find_element(By.NAME, 'password')
        # password_field.send_keys(password)
        # password_field.send_keys(Keys.ENTER)
        # time.sleep(5)



    