# whatsTrack

<!-- > Looking down the misty path to uncertain destinations🌌🍀&nbsp;&nbsp;&nbsp;<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- x' <br><br><br> -->

It is online tracker for whatsapp.
It tracks if user is online or offline regardless of their last seen been hidden. But it must run continously for that.

<br>

## Requirements
* Linux 4.18+
* Viewnior
  * Image viewer for linux
* Selenium
  * A web automation framework (Here as python library)
* Geckodriver 0.24.0 https://github.com/mozilla/geckodriver/releases
  * A web browser engine used in the link between your tests in Selenium and the Firefox browser
* Firefox 68.0+
* Python 3
* Numpy
* Matplotlib



### Arch Linux

```sh
$ sudo pacman -S firefox
$ sudo pacman -S viewnior
$ sudo pacman -S python
$ sudo pacman -S python-pip
$ sudo pip install numpy
$ sudo pip install matplotlib
$ sudo pip install selenium
```

### Ubuntu

```sh
$ sudo apt install firefox
$ sudo apt install viewnior
$ sudo apt install python3
$ sudo apt install python3-pip
$ pip3 install numpy
$ pip3 install matplotlib
$ pip3 install selenium
```

## Usage

python3 whatsTrack <i>number</i> <i>name</i><br>
python whatsTrack <i>number</i> <i>name</i>


## Working

Selenium is a web automation framework for automating clicks or inputs on browser<br>
Geckodriver gives implementation for automation for firefox<br>
whatsTrack opens headless(without gui or any front window) firefox window and opens [WhatsApp Web](https://web.whatsapp.com/)<br>
It will ask you to scan QR code to link your WhatsApp with browser where it will go to one's chatbox and continously monitor if one is online or not seeing their status and store it in file <i>time.csv</i> manchaster encoded


### WhatsApp Web Elements List

| Class ID | Element |
| -------- | ------- |
| _28BNY   | <img src = https://github.com/pushpull13/whatsTrack/blob/master/img/turn_on_notify.png> <br> <img src = https://github.com/pushpull13/whatsTrack/blob/master/img/computer_not_connected.png> <br> <img src = https://github.com/pushpull13/whatsTrack/blob/master/img/phone_not_connected.png> |
| _2zCfw   | <img src = https://github.com/pushpull13/whatsTrack/blob/master/img/search.png> |
| _19RFN   | <img src = https://github.com/pushpull13/whatsTrack/blob/master/img/chat.png> |
| _315-i   | <img src = https://github.com/pushpull13/whatsTrack/blob/master/img/online.png> |


<br><br>

### Set URL

Set url to WhatsApp Web
```python
url = "https://web.whatsapp.com/"
```
<br>

### Launch browser

Set headless option for firefox and opens blank firefox window

```python
options = Options()
options.headless=True
window = webdriver.Firefox(options=options, executable_path='geckodriver', firefox_binary=FirefoxBinary('firefox'))
```

<br>

### Load page

Load WhatsApp Web

```python
window.get(url)
```

<br>

### Save live page in browser

Save screenshot of current window<br>
Scan QR code and close <i>viewnior</i> to continue

```python
window.save_screenshot('qr.png')
qr_code = plt.imread('qr.png')
plt.imshow(qr_code)

fish.call(["viewnior", "qr.png"])
```

<br>

### Wait to load page

Wait until HTML element <i>_28BNY</i> loads

```python
while(True):
    try:
        page_loaded = window.find_element_by_class_name("_28Bny")
        print("Page fully loaded")
        break
    except:
        print("Page loading...")
        time.sleep(1)
```

<br>

### Search for search box

Find search box on page <br>
Element ID = _2zCfw

```python
element = window.find_element_by_class_name("_2zCfw")
```

<br>

### Enter number in search box

Click on search box and search for given number

```python
element.click()
element.send_keys(number)
```

<br>

### Open chat

Find element of given person name and click on it to open chat

```python
element = window.find_elements_by_class_name("_19RFN")

for i in range(len(element)):
    if element[i].get_attribute("title") == name:
        element[i].click()
```

<br>

### Online check

Check if person is online

```python
def isOnline():
    try:
        online = window.find_element_by_class_name("_315-i")
        if online.get_attribute("title") == "online":
            online_status = True
        else:
            online_status = False
    except:
        online_status = False
    return online_status
```

<br>

### Start tracking

Starts infinite loop for continously tracking person and prints time in <i>time.csv</i> file only if either comes offline to online or goes offlline from online (Manchester Encoding)

```python
while True:
    file = open("time.csv", "a")
    curr_time = datetime.datetime.now()
    date_time = curr_time.strftime("%d/%m/%Y,%H:%M:%S")
    live = live_page()
    if isOnline():
        if prev_status == False:
            file.write("\n")
            file.write(date_time)
            file.write(",")
            file.write("1")
            print(date_time + "   " + number + " came online")
            prev_status = True
        print(date_time + "   " + number + " is online")
    else:
        if prev_status == True:
            file.write("\n")
            file.write(date_time)
            file.write(",")
            file.write("0")
            print(date_time + "   " + number + " went offline")
            prev_status = False
#        print(number + " is offline")
    file.close()
    time.sleep(1)
```
