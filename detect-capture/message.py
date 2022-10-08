from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import time
import os
import telepot

telegram_bot = telepot.Bot(token="")

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
chromedriver = "/usr/bin/chromedriver"

facebook_user_link = "https://www.messenger.com/t/100079285037181"

facebook_bot_username = 'lorcaphan@gmail.com'
facebook_bot_password = 'Longphan0612'

telegram_chat_id1 = '1921540131'
telegram_chat_id2 = '5335298143'

def messenger(user_link):
    
    driver = webdriver.Chrome(chromedriver, 
                              chrome_options=options)

    driver.get("https://www.messenger.com/login/")

    time.sleep(2)

    username = driver.find_element_by_id('email')
    username.send_keys(facebook_bot_username)

    password = driver.find_element_by_id('pass')
    password.send_keys(facebook_bot_password)

    login = driver.find_element_by_id('loginbutton')
    login.click()
    
    driver.get(user_link)
    
    time.sleep(8)
    
    # pyautogui.write("[ALERT] Detected someone in the frame!")
    
    # time.sleep(2)

    # pyautogui.press('enter')
    
    
    os.system(f"xclip -selection clipboard -t image/png -i {'~/RPI-People-Detection' + '/image.png'}")
    
    pyautogui.hotkey('ctrl', 'v')
    
    time.sleep(5)

    pyautogui.press('enter')
    
    time.sleep(2)
    
def telegram(chat_id):
    
    # Me: 1921540131
    # Mom: 5335298143
    
    # telegram_bot.sendMessage(chat_id=chat_id,
#                 text="[ALERT] Detected someone in the frame!")

    telegram_bot.sendPhoto(chat_id=chat_id,
                photo=open("image.png", "rb"))


