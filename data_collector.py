from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from configparser import ConfigParser
import mysql.connector
import time
import random
from datetime import datetime, timedelta

LINKS = ["https://discord.com/channels/---"]  # WRITE DISCORD SERVER URLs HERE

#------------------CONFIG---------------------
config_object = ConfigParser()
config_object.read("config.ini")
account = config_object["DISCORDACCOUNT"]
serverconfig = config_object["SETTINGS"]
DCMAIL = account["MAIL"]
DCPASSWORD = account["PASSWORD"]
LOGINPAGE = serverconfig["LOGINPAGE"]
DAYSBEFORE = serverconfig["DAYSINCE"]
CHROMEDRIVERPATH = serverconfig["CHROMEDRIVERPATH"]
NEXTBUTTONPATH = serverconfig["NEXTBUTTONPATHS"]
EMAILIDNAME = serverconfig["EMAILIDNAME"]
PASSWORDIDNAME = serverconfig["PASSWORDIDNAME"]
CONTINUEXPATH = serverconfig["CONTINUEXPATH"]
SEARCHXPATH = serverconfig["SEARCHXPATH"]
SEARCHXPATHCONT = serverconfig["SEARCHXPATHCONT"]
RESULTXPATH = serverconfig["RESULTXPATH"]
RESULTID = serverconfig["RESULTID"]

#---------------------------------------------
keyDate = datetime.now() - timedelta(days= int(DAYSBEFORE))
keyDate.strftime('%Y-%m-%d')
keyString = "after:" + str(keyDate)
keyString = keyString.split(' ', 1)[0]
print(keyString)
yesterday = datetime.now() - timedelta(days=1)
yesterday.strftime('%m/%d/%Y')
today = time.strftime('%m/%d/%Y')

def timerandomizer():
    # returns a float between 0.1 - 0.4
    # this function used with time.sleep in order to prevent discord from detecting bot activity
    x = float(random.randint(1,5)) / 10
    return x

driver = webdriver.Chrome(CHROMEDRIVERPATH)
driver.get(LOGINPAGE)

#--------------Login Part---------------------
search = driver.find_element_by_name(EMAILIDNAME)
search.send_keys(DCMAIL)
time.sleep(timerandomizer())

search = driver.find_element_by_name(PASSWORDIDNAME)
search.send_keys(DCPASSWORD)
time.sleep(timerandomizer())

search.send_keys(Keys.RETURN)
#---------------------------------------------
counter = 0

#-------------Channel Surf--------------------
for link in LINKS:
    time.sleep(1)
    try:
        driver.get(link)
    except:
        # can not reach link
        pass
    time.sleep(3)

    try:
        continueButton = driver.find_element_by_xpath(CONTINUEXPATH)
        time.sleep(timerandomizer())
        continueButton.click()
    except:
        # do not have nsfw button (continue without problem)
        pass
    time.sleep(1)
    resultlist = []
    try:
        search = driver.find_element_by_xpath(SEARCHXPATH)
        time.sleep(timerandomizer())
        search.send_keys(keyString)
        search = driver.find_element_by_xpath(SEARCHXPATHCONT)
        search.send_keys(Keys.RETURN)
        time.sleep(3)
        try:
            element = driver.find_element_by_id(RESULTID)

            # ----------------Data Shuffling-----------------
            for line in str(element.text).splitlines():
                if not line.startswith('#'):
                    resultlist.append(line)
        except:
            pass
    except:
        pass
    try:
        nextButton = driver.find_element_by_xpath(NEXTBUTTONPATH)
        nextEnabled = driver.find_element_by_xpath(NEXTBUTTONPATH).is_enabled()
    except:
        nextEnabled = False

    while(nextEnabled):
        nextButton.click()
        time.sleep(2)
        try:
            element = driver.find_element_by_id(RESULTID)
            # ----------------Data Shuffling-----------------
            for line in str(element.text).splitlines():
                if not line.startswith('#'):
                    resultlist.append(line)
        except:
            pass
        try:
            nextButton = driver.find_element_by_xpath(NEXTBUTTONPATH)
            nextEnabled = driver.find_element_by_xpath(NEXTBUTTONPATH).is_enabled()
        except:
            nextEnabled = False
        print(nextEnabled)
    when = ""
    message = ""
    user = ""
    firstTime = True
    for i in resultlist:
        if i == "BOT":
            resultlist.remove(i)
    for i in range(len(resultlist)):
        if("Today at" in resultlist[i] or "Yesterday at" in resultlist[i] or (len(resultlist[i]) == 10 and str(resultlist[i][2]) == "/" and str(resultlist[i][5]) == "/")):
            if(firstTime):
                if ("Today at" in resultlist[i]):
                    when = today
                elif ("Yesterday at" in resultlist[i]):
                    when = yesterday
                else:
                    when = resultlist[i]
                user = resultlist[i - 1]
                message = ""
                firstTime = False
            elif not firstTime:
                message = message[:len(message) - len(resultlist[i - 1])]
                print("time: ", when)
                print("user: ", user)
                print("message: ", message)
                if("Today at" in resultlist[i]):
                    when = today
                elif("Yesterday at" in resultlist[i]):
                    when = yesterday
                else:
                    when = resultlist[i]
                user = resultlist[i - 1]
                message = ""
        else:
            message += resultlist[i]
    time.sleep(1)
#---------------------------------------------