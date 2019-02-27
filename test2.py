import time
import numpy as np
from random import uniform

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent

from win10toast import ToastNotifier

TIME_OUT = 60 * 60 * 2  # time out for trying to get a booking (2 hours)
SLEEP_TIME = 60 * 60 * 2  # sleep time after reaching the page for booking (2 hours)

HAUTS_DE_SEINE_GOUV_FR = "http://www.hauts-de-seine.gouv.fr/booking/create/4462/0"

def return_twodecimalstime():
    return np.around(uniform(1,2), decimals=2)

def selenium_naturalisation():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    #options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    #browser = webdriver.Chrome(chrome_options=options)
    #options = Options()
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    options.add_argument(f'user-agent={userAgent}')
    #driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\WebDrivers\ChromeDriver\chromedriver_win32\chromedriver.exe')
    browser = webdriver.Chrome(chrome_options=options)

    send_notification = False
    timeout = time.time() + TIME_OUT

    time.sleep(return_twodecimalstime())
    browser.get(HAUTS_DE_SEINE_GOUV_FR)
    while (not send_notification and time.time() < timeout):

        time.sleep(return_twodecimalstime())
        # refresh while the page does not load
        condition_element = None
        while condition_element is None:
            try:
                condition_element = browser.find_element_by_id("condition")
            except NoSuchElementException:
                pass

        position = condition_element.location

        # issue with chrome driver, need to scroll manually to the location
        browser.execute_script("window.scrollTo(" + str(position['x']) + ", " + str(position['y']) + ")")

        time.sleep(return_twodecimalstime())

        # click on check box to accept condition
        condition_element.click()

        time.sleep(return_twodecimalstime())

        # click on next
        browser.find_element_by_name("nextButton").click()

        time.sleep(return_twodecimalstime())

        # choisir un champ
        #element = None
        element = browser.find_element_by_id("planning7070")

        time.sleep(return_twodecimalstime())
        browser.execute_script("arguments[0].click();", element)
        # click on next
        browser.find_element_by_name("nextButton").click()

        time.sleep(return_twodecimalstime())
        # check if that there are no booking date
        try:
            form = browser.find_element_by_id("FormBookingCreate")
            if not form or not("Veuillez recommencer" in form.text or "Please try later" in form.text):
                # no form? or not the annoying message? send notification
                send_notification = True
            else:
                # retry in 1 second
                time.sleep(return_twodecimalstime())
                browser.find_element_by_name("finishButton").click()
        except NoSuchElementException:
            # the element does not exist? notify
            send_notification = True

    if send_notification:
        toaster = ToastNotifier()
        toaster.show_toast("Selenium naturalisation","Go check chrome!!!", duration=60)
        time.sleep(SLEEP_TIME)  # wait until the user has finished using the browser


if __name__ == '__main__':
    selenium_naturalisation()
