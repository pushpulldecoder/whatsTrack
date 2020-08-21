#%%
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import pickle
import sys
import signal
from matplotlib import pyplot as plt
import numpy as np
import time
import subprocess as fish
import datetime


#%%
def ctrlC(sig, frame):
    print("Saving Cookies and terminating in")
    time.sleep(1)
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    inp = input()
    if inp=="x":
        exit(0)
    elif inp=="c":
        play = 1
    elif inp=="n":
        play = 0

signal.signal(signal.SIGINT, ctrlC)


number = sys.argv[1]
name   = sys.argv[2]


print("Tracker initializing for " + name)
fish.call(["notify-send", "Tracker initilizing for", name, "-i", "/home/pushpull/mount/intHdd/Project/whatsTrack_2_0/whatsApp.png"])

#%%
print("Setting URL to https://web.whatsapp.com")
url = "https://web.whatsapp.com/"

#%%
options = Options()
#options.log.level = "fatal"
options.headless=True

#%%
print("Staring headless firefox window")
window = webdriver.Firefox(options=options, executable_path='geckodriver', firefox_binary=FirefoxBinary('firefox'))

#%%
print("Scan the QR code from mobile within 5 seconds")
fish.call(["notify-send", "Scan the QR code from mobile within 5 seconds", "-i", "/home/pushpull/mount/intHdd/Project/whatsTrack_2_0/whatsApp.png"])
time.sleep(5)
print("Connecting to https://web.whatsapp.com")
window.get(url)

#%%
window.save_screenshot('qr.png')
qr_code = plt.imread('qr.png')
plt.imshow(qr_code)

fish.call(["viewnior", "qr.png"])

#%%
def playSOS():
    fish.call(["sh", "./playSOS.sh"])

def playBeep():
    fish.call(["sh", "./playBeep.sh"])

def playStop():
    fish.call(["sh", "./playStop.sh"])



#%%
def live_page():
    window.save_screenshot('live.png')
    live = plt.imread('live.png')
    return live

#%%
print("Current window")
live = live_page()
plt.imshow(live)
fish.call(["viewnior", "live.png"])

#%%


def waitToLoad():
    print("Waiting for page to load...")
    while(True):
        try:
            page_loaded = window.find_element_by_class_name("_2S1VP")
            fish.call(["notify-send", "WhatsApp Web fully loaded", "-i", "/home/pushpull/mount/intHdd/Project/whatsTrack_2_0/whatsApp.png"])
            print("WhatsApp Web fully loaded")
            playBeep()
            break
        except:
            print("WhatsApp Web loading...")
            live_page()
            time.sleep(1)
#%%
waitToLoad()

#%%

def findName():
    element = window.find_element_by_class_name("_2S1VP")
    element.click()
    element.send_keys(number)

#%%
findName()

#%%
print("Current window")
live = live_page()
fish.call(["viewnior", "live.png"])

#%%
def clickOnName():
    element = window.find_elements_by_class_name("_1wjpf")

    for i in range(len(element)):
        if element[i].get_attribute("title") == name:
            print("Yo... Clicked")
            element[i].click()

#%%
clickOnName()

#%%
print("Waiting for 20 seconds...")
time.sleep(20)

#%%
live = live_page()
fish.call(["viewnior", "live.png"])
#%%
prev_status = False
status_changed = False

#%%

def isOnline():
    try:
        online = window.find_element_by_class_name("O90ur")
        if online.get_attribute("title") == "online":
            online_status = True
        else:
            online_status = False
    except:
        online_status = False
    return online_status

#%%
print("\n\n\n")
print("Tracking for " + name)
print("\n\n\n")

curr_time = datetime.datetime.now()
date_time = curr_time.strftime("%d/%m/%Y,%H:%M:%S")

file = open("time.csv", "a")
file.write("\n")
file.write(date_time)
file.write(",0")
file.close()

play = 0

time.sleep(1)

while True:

    dualWindow = element = window.find_elements_by_class_name("_1WZqU")
    if len(dualWindow)!=0:
        live = live_page()
        for i in range(180):
            live = live_page()
            print("Wait for ", 180-i, " seconds")
            time.sleep(1)
        dualWindow[1].click()
        waitToLoad()
        findName()
        clickOnName()

    file = open("time.csv", "a")
    curr_time = datetime.datetime.now()
    date_time = curr_time.strftime("%d/%m/%Y,%H:%M:%S")
    live = live_page()
    if isOnline():
        if play==1:
            playBeep()
        if prev_status == False:
            playSOS()
            file.write("\n")
            file.write(date_time)
            file.write(",")
            file.write("1")
            notification = "x'" + " came online"
            fish.call(["notify-send", notification, "-i", "./whatsApp.png"])
            print(date_time + "   " + "x'" + " came online")
            prev_status = True
        print(date_time + "   " + "x'" + " is online")
    else:
        if prev_status == True:
            playStop()
            file.write("\n")
            file.write(date_time)
            file.write(",")
            file.write("0")
            notification = "x'" + " went offline"
            fish.call(["notify-send", notification, "-i", "./whatsApp.png"])
            print(date_time + "   " + "x'" + " went offline")
            prev_status = False
#        print(number + " is offline")
    file.close()
    time.sleep(1)


