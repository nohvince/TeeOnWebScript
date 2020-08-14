from selenium import webdriver
import datetime
import os

GOOGLE_CHROME_PATH = os.environ['GOOGLE_CHROME_BIN']
CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']

TIME_TO_BOOK = '11:00' # 24hr format hh:mm
EIGHTEEN_HOLES = True
NUM_PLAYERS = 4

DATE_TO_BOOK = datetime.date.today() + datetime.timedelta(days=5)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
if GOOGLE_CHROME_PATH != "":
    chrome_options.binary_location = GOOGLE_CHROME_PATH

browser = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
browser.get('https://www.tee-on.com/PubGolf/servlet/com.teeon.teesheet.servlets.golfersection.WebBookingSearchSteps?CourseGroupID=12&BackTarget=/')
browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/div/div/div/div/div/div/form/div[1]/select/option[7]').click()

time_options = browser.find_element_by_xpath('//*[@id="SearchTime"]')
for option in time_options.find_elements_by_tag_name('option'):
    if option.get_attribute('value') == TIME_TO_BOOK:
        option.click()

if EIGHTEEN_HOLES:
    browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/div/div/div/div/div/div/form/div[3]/div/div/label[1]').click()
else:
    browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/div/div/div/div/div/div/form/div[3]/div/div/label[2]').click()

