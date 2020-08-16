from selenium import webdriver
from time import sleep
import datetime
import DateTime
import os
import re

GOOGLE_CHROME_PATH = os.environ['GOOGLE_CHROME_BIN']
CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']

TIME_TO_BOOK = '11:00' # 24hr format hh:mm
EIGHTEEN_HOLES = False
NUM_PLAYERS = 1
LOWER_BOUND_TIME = '9:00'
UPPER_BOUND_TIME = '20:00'

USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
LOGIN_PAGE_REGEX = '.*SignInGolferSection.*'
CART_PAGE_REGEX = '.*WebBookingChooseCarts.*'
SEARCH_RESULTS_REGEX = '.*WebBookingSearchResults.*'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
if GOOGLE_CHROME_PATH != "":
    chrome_options.binary_location = GOOGLE_CHROME_PATH

browser = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=chrome_options)
browser.get('https://www.tee-on.com/PubGolf/servlet/com.teeon.teesheet.servlets.golfersection.WebBookingSearchSteps?CourseGroupID=12&BackTarget=/')

# Select 5 days from now
DATE_TO_BOOK = datetime.date.today() + datetime.timedelta(days=5)
dates_cont = browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/div/div/div/div/div/div/form/div[1]/select')
dates = dates_cont.find_elements_by_tag_name('option')
for date in dates:
    if date.get_attribute('value') == str(DATE_TO_BOOK):
        date.click()
        break

# Select preferred time
time_options = browser.find_element_by_xpath('//*[@id="SearchTime"]')
for option in time_options.find_elements_by_tag_name('option'):
    if option.get_attribute('value') == TIME_TO_BOOK:
        option.click()

# Select num holes
if EIGHTEEN_HOLES:
    browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/div/div/div/div/div/div/form/div[3]/div/div/label[1]').click()
else:
    browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/div/div/div/div/div/div/form/div[3]/div/div/label[2]').click()

# Select num of players
players_div = browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/div/div/div/div/div/div/form/div[4]/div/div')
num_players_btn = list(filter(lambda btn: btn.get_attribute('for') == 'toggle-' + str(NUM_PLAYERS), players_div.find_elements_by_tag_name('label')))
for btn in num_players_btn:
    btn.click()

# Location Toronto and Area
browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/div/div/div/div/div/div/form/div[5]/div/select/optgroup[9]/option[42]').click()

# Select course
browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/div/div/div/div/div/div/form/div[5]/div/div[1]/div/div/table/tbody/tr[8]/td[1]/label/span').click()


# Go to next page
browser.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/div/div/div/div/div/div/div/form/a[2]').click()

# Select closest time
container = browser.find_element_by_class_name('search-results-tee-times-wrapper')
times = container.find_elements_by_class_name('search-results-tee-times-box')
good_times = []

LOWER_BOUND_HOUR = int(LOWER_BOUND_TIME.split(':')[0])
LOWER_BOUND_MIN = int(LOWER_BOUND_TIME.split(':')[1])
UPPER_BOUND_HOUR = int(UPPER_BOUND_TIME.split(':')[0])
UPPER_BOUND_MIN = int(UPPER_BOUND_TIME.split(':')[1])
for time_con in times:
    time = time_con.find_element_by_class_name('time').text
    time_split = time.split(':')
    hour = int(time_split[0]) if time_con.find_element_by_class_name('am-pm').text.lower() == 'am' else (12 if int(time_split[0]) == 12 else int(time_split[0]) + 12)
    min = int(time_split[1][0:2])

if ((hour == LOWER_BOUND_HOUR and min >= LOWER_BOUND_MIN) or (hour > LOWER_BOUND_HOUR)) and ((hour < UPPER_BOUND_HOUR) or (hour == UPPER_BOUND_HOUR and min <= UPPER_BOUND_MIN)):
    good_times.append(time_con)

time_split = TIME_TO_BOOK.split(':')[0]
hour = time_split[0]
pref_time_is_morn = True
if int(hour) > 12:
    pref_time_is_morn = False
    hour = str(int(hour) - 12)

pref_secs = DateTime.DateTime('1997/8/8 ' + hour + ':' + time_split[1] + ('am' if pref_time_is_morn else 'pm')).timeTime()

closest_time_container = 0
closest_time_secs = 0
closest_time = 0
for time in good_times:
    time_val = str(time.find_element_by_class_name('time').text)
    secs = DateTime.DateTime('1997/8/8 ' + time_val).timeTime()
    diff = abs(secs - pref_secs)

if closest_time_container == 0:
    closest_time_container = time
    closest_time_secs = diff
    closest_time = time_val
elif diff < closest_time_secs:
    closest_time_container = time
    closest_time_secs = diff
    closest_time = time_val

if closest_time_container != 0:
    try:
        closest_time_container.find_element_by_class_name('details-btn').click()
    except:
        closest_time_container.find_element_by_class_name('book-btn').click()
else:
    print('No times found in given range')

# Not sure how Don Valley selection behaves (whether it goes direct to login or brings up popup). Deal with both cases
search = re.compile(SEARCH_RESULTS_REGEX)
carts = re.compile(CART_PAGE_REGEX)
login = re.compile(LOGIN_PAGE_REGEX)

count = 0
max_attempts = 3
while not re.match(login, browser.current_url):
    sleep(0.5)
    count += 1
    if re.match(carts, browser.current_url):
        browser.find_element_by_xpath('/html/body/div[6]/div[1]/div[2]/div/div/div/div/div/div/div/div[2]/form/div/div/label[1]').click()
        browser.find_element_by_xpath('/html/body/div[6]/div[1]/div[2]/div/div/div/div/div/div/div/a[2]').click()
    elif re.match(search, browser.current_url):
        p = re.compile('.*' + str(closest_time) + '.*')
        popups = browser.find_elements_by_class_name('GenericPopup')
        found_popup = False

        for popup in popups:
            elements = popup.find_elements_by_xpath(".//*")

            for element in elements:
                if re.match(p, element.text):
                    found_popup = True

            if found_popup:
                popup.find_element_by_xpath('.//div/a[2]').click()
                break

    if count >= max_attempts:
        print("Reached max attempts to reach login page")
        break

sleep(0.5)

# Login
browser.find_element_by_xpath('//*[@id="Username"]').send_keys(USERNAME)
browser.find_element_by_xpath('//*[@id="Password"]').send_keys(PASSWORD)
browser.find_element_by_xpath('//*[@id="sign-in-btn"]').click()

# Click past last confirmation pages (note doesn't know how to handle the required payment page
try:
    browser.find_element_by_xpath('/html/body/div[16]/div[1]/div[2]/div/div/div/div/div/div/div/a[2]').click()
except:
    browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/div/div/a[2]').click()

try:
    browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div/div/div/div/div/div/div/a[2]').click()
except:
    print("No need for second selection page")

browser.quit()