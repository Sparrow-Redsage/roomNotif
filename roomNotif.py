#Author: Venzah Hamilton

"""
1. Download
2. Open terminal
3. source .venv/bin/activate
4. python3 roomNotif.py
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from time import sleep
import datetime
import schedule


def navigate_home_page(driver):
    driver.get("https://book.passkey.com/event/51137237/owner/54055/home")

    # Checks link opens the correct home page
    assert "Katsucon Entertainment" in driver.title
    assert "Start your reservation" in driver.title

    cookie_banner = driver.find_element(By.ID, "acceptAllBtn")
    cookie_banner.click()

    """
    Note: When opening the page, a banner about accepting cookies will pop up. "Okay" will need to be clicked first, otherwise
    selecting will be blocked. Couldn't really find a nicer alternative besides having the program sleep while the cookie banner
    is being dismissed.
    """
    sleep(3)

    select_element = driver.find_element(By.ID, "groupTypeId")
    select = Select(select_element)
    select.select_by_visible_text("Attendee")

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "submit-btn"))).click()

    sleep(3)


def navigate_booking_page(driver):
    # Checks button opens the correct booking page 
    assert "Katsucon Entertainment" in driver.title
    assert "Learn about the event and search for hotels" in driver.title

    #Open the start date box and select feb 11
    sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/form/div[1]/ul/li[1]/h5").click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "dp_in_1_11"))).click()

    #Open the end date box and select feb 14 as the end date
    sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/form/div[1]/ul/li[2]/h5").click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "dp_out_1_14"))).click()

    number = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/form/div[1]/ul/li[4]/div[1]/div[2]/span/a[1]")
    for i in range(3):
        number.click()

    driver.find_element(By.ID, "submitQuickBook").click()

    sleep(3)


def check_availability(driver):
    try:
        #assert "No room matched your search criteria" in driver.page_source
        driver.find_element(By.XPATH, "//*[@id='errMsg']")
    except NoSuchElementException:
        print("Match!")
        interrupt = ""
        while interrupt != "Y":
            print("Done: ")
            interrupt = input()
        return True

    print("Nothing!")
    return False
    
def find_open_rooms():
    print("Checking availability at:", datetime.datetime.now())
    driver = webdriver.Firefox()
    navigate_home_page(driver)
    navigate_booking_page(driver)
    check_availability(driver)
    driver.quit()


if __name__ == "__main__":
    schedule.every().minute.at(":00").do(find_open_rooms)

    try:
        while True:
            schedule.run_pending()
            sleep(1)
    except KeyboardInterrupt:
        pass

    
    
    
    
    