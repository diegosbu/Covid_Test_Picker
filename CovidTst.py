# Imports
from dotenv import load_dotenv
load_dotenv()
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)

from datetime import date, timedelta
import time

# BU login credentials
userInput = os.environ.get("user")
passInput = os.environ.get("pass")

# dateGen: Chooses next closest Friday date
def dateGen(choseDay):
    choseDay = date.today()
    extraDay = timedelta(days = 1)

    prod = 4 - choseDay.weekday()

    if prod == -1:
        prod = 6
    elif prod == -2:
        prod = 5

    choseDay += (extraDay*prod)

    friMonth = choseDay.month
    friDay = choseDay.day
    friYear = choseDay.year

    friDate = str("%02d" % friMonth) + str("%02d" % friDay) + str(friYear)

    return friDate

# set equal to friDate
apptDate = dateGen(date.today())

# Fills out forms/prompts prior to appointment search
driver.get("https://patientconnect.bu.edu")

username = driver.find_element(By.ID, "j_username")
passwrd = driver.find_element(By.ID, "j_password")
submit = driver.find_element(By.CLASS_NAME, "input-submit")

username.send_keys(userInput)
passwrd.send_keys(passInput)
submit.click()

driver.get("https://patientconnect.bu.edu/appointments_home.aspx")

schedule = driver.find_element(By.ID, "cmdSchedule")
schedule.click()

option = driver.find_element(By.ID, "297")
option.click()
proceed = driver.find_element(By.ID, "cmdProceed")
proceed.click()

testing = driver.find_element(By.ID, "496")
testing.click()
proceed = driver.find_element(By.ID, "cmdProceed")
proceed.click()

consent = driver.find_element(By.ID, "493")
consent.click()
proceed = driver.find_element(By.ID, "cmdProceed")
proceed.click()

consent2 = driver.find_element(By.ID, "484")
consent2.click()
proceed = driver.find_element(By.ID, "cmdProceed")
proceed.click()

confirm = driver.find_element(By.ID, "478")
confirm.click()
proceed = driver.find_element(By.ID, "cmdProceed")
proceed.click()

confirm2 = driver.find_element(By.ID, "498")
confirm2.click()
proceed = driver.find_element(By.ID, "cmdProceed")
proceed.click()

proceed2 = driver.find_element(By.ID, "cmdStandardProceed")
proceed2.click()


# Sets date for appointment search
calendar = driver.find_element(By.ID, "StartDate")
calendar.send_keys(Keys.CONTROL + "a")
calendar.send_keys(Keys.DELETE)
calendar.send_keys(apptDate[:2])
calendar.send_keys(apptDate[2])
calendar.send_keys(apptDate[3])
calendar.send_keys(apptDate[4])
calendar.send_keys(apptDate[5])
calendar.send_keys(apptDate[6])
calendar.send_keys(apptDate[7])

# Chooses location for appointment
GalleryLoc = driver.find_element(By.XPATH, "//select[@id='LocationList']/option[@value='51']")
GalleryLoc.click()

confirmAppt = driver.find_element(By.ID, "apptSearch")
confirmAppt.click()

# Iterates through available appointments table
apptRows = driver.find_elements(By.XPATH, "//table[@class='appt-list table table-striped table-responsive']/tbody/tr")
friDates = []

# Parses table for all Friday appointments
for i in apptRows:
    if "Friday" in ((i.get_attribute('innerText')).strip()):
        friDates.append(i)

# Chooses latest appointment available on Friday
selection = friDates[-1].find_element(By.TAG_NAME, "input")
selection.click()

# Confirms appointment selection
confirmDate = driver.find_element(By.ID, "cmdStandardProceed")
confirmDate.click()

finalConfirm = driver.find_element(By.ID, "cmdConfirm")
finalConfirm.click()

driver.quit()
