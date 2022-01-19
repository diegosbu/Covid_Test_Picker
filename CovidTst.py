# Imports
from dotenv import load_dotenv
load_dotenv()
import os

from datetime import date, timedelta
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# BU login credentials
userInput = os.environ.get("user")
passInput = os.environ.get("pass")


# Converts day to .weekday() output
weekDays = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}

# Input desired appointment day
desireDay = input("What day of the week do you want your covid test?: ")
desireDay = desireDay.capitalize()

# dateGen: returns date of next closest desired weekday
def dateGen(choseDay):
    currDay = date.today()
    extraDay = timedelta(days = 1)

    while currDay.weekday() != weekDays["Friday"]:
        currDay += extraDay        

    desireMon = currDay.month
    desireDay = currDay.day
    desireYr = currDay.year

    desireDate = str("%02d" % desireMon) + str("%02d" % desireDay) + str(desireYr)

    return desireDate

# Set equal to desired date
apptDate = dateGen(desireDay)


# Initalizes Selenium Chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)

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
apptTimes = []

# Parses table for all desired date appointments
for i in apptRows:
    if desireDay in ((i.get_attribute('innerText')).strip()):
        apptTimes.append(i)

# Chooses latest appointment available on Friday
selection = apptTimes[-1].find_element(By.TAG_NAME, "input")
selection.click()

# Confirms appointment selection
confirmDate = driver.find_element(By.ID, "cmdStandardProceed")
confirmDate.click()

finalConfirm = driver.find_element(By.ID, "cmdConfirm")
finalConfirm.click()

print("Appointment set!")

driver.quit()
