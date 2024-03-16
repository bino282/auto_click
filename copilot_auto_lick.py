import pyautogui
pyautogui.FAILSAFE = False
import time
import settings
import cv2
import numpy as np
import pyperclip
from sql_cli import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests
def change_ip():
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NWYxMjhmZWI1M2EwMjBhNWM3YTlkMTAiLCJpYXQiOjE3MTAzNDEyMjcsImV4cCI6MTcxMjkzMzIyN30.hWa0C2Q9jhSGgNBoPE_IBIWdIFwxILEMvU6_dUX7Rj0"}
    res = requests.get("https://api.zingproxy.com/proxy/dan-cu-viet-nam/get-ip?sourceId=ZP24096_66209&location=Random",headers=headers).json()
    return res
def enter_proxy_auth():
    time.sleep(1)
    pyperclip.copy('nha28_HfkqY')
    with pyautogui.hold('ctrl'):
        pyautogui.press(['v'])
    pyautogui.press('tab')
    pyperclip.copy('PT1cgwy5')
    with pyautogui.hold('ctrl'):
        pyautogui.press(['v'])
    pyautogui.press('enter')
PROXY = "http://116.111.110.252:29673"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--proxy-server=%s' % PROXY)
service = Service(executable_path=r"./driver/chromedriver.exe")
driver = webdriver.Chrome(service=service,options=chrome_options)
driver.implicitly_wait(2)
driver.maximize_window()


def find_button_location(button_img_path,THRESHOLD=0.8):
    # take screenshot
    img = pyautogui.screenshot()
    
    # find copy btn location
        
    screen_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    button_img = cv2.imread(button_img_path, cv2.IMREAD_GRAYSCALE)
    w_img, h_img = screen_img.shape[1], screen_img.shape[0]
    w, h = button_img.shape[1], button_img.shape[0]
    result = cv2.matchTemplate(screen_img, button_img, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= THRESHOLD)
    rx, ry = 0, 0
    #Draw boudning box
    for y, x in zip(loc[0], loc[1]):
        # cv2.rectangle(orig_img, (x, y), (x + w, y + h), (0,0,255), 4)
        rx = int(x + w/2)
        ry = int(y + h/2)
        break
    return rx, ry

def input_prompt(prompt):
    # enter_x, enter_x = find_button_location("./icons/enter.jpg",THRESHOLD=0.9)
    enter_x, enter_y = 715, 960
    pyautogui.click(enter_x, enter_y)
    time.sleep(1)
    with pyautogui.hold('ctrl'):
        pyautogui.press('a')
    pyautogui.press('delete')
    pyperclip.copy(prompt)
    
    with pyautogui.hold('ctrl'):
        pyautogui.press(['v'])
    
    pyautogui.typewrite(['enter'])
    pyautogui.moveTo(enter_x-600, enter_y-100)
    time.sleep(5)
    pyautogui.scroll(-500)
    human_x , human_y = find_button_location("./icons/human.jpg")
    if human_x!=0 and human_y!=0:
        print(human_x, human_y)
        pyautogui.click(human_x, human_y, duration=1)
    pyautogui.scroll(-500)
    while(True):
        time.sleep(5)
        status_x , status_y = find_button_location("./icons/status.jpg")
        if status_x == 0 and status_y == 0:
            break
    pyautogui.scroll(-5000)
    time.sleep(1)
    continue_x, continue_y = find_button_location("./icons/continue.jpg")
    if continue_x!=0 or continue_y!=0:
        pyautogui.click(continue_x, continue_y, duration=1)
        time.sleep(1)
    pyautogui.scroll(-500)
    time.sleep(1)
    count = 0
    while(True):
        count = count + 1
        if count > 10:
            return False
        copy_x, copy_y = find_button_location("icons/co_option.jpg")
        if copy_x == 0 and copy_y == 0:
            pyautogui.scroll(200)
            time.sleep(1)
        else:
            break
    if copy_x == 0 and copy_y == 0:
        return False
    pyperclip.copy(' ')
    pyautogui.click(copy_x, copy_y, duration=1)
    time.sleep(5) 
    text = pyperclip.paste()
    if text == ' ':
        return False
    return text

import hashlib

def string_to_id(input_string):
    hash_object = hashlib.md5(input_string.encode())
    return hash_object.hexdigest()

if __name__ == "__main__":
    import ndjson, json, os
    from datetime import datetime
    import random
    name = "CodeFeedback-Filtered-Instruction"
    with open(f"data/{name}.jsonl","r",encoding="utf-8") as fr:
        data = ndjson.load(fr)
    random.shuffle(data)
    url = "https://copilot.microsoft.com/"
    driver.get(url)
    enter_proxy_auth()
    time.sleep(5)
    new_x, new_y = find_button_location("./icons/new.jpg")
    if new_x == 0 and new_y ==0:
        print("new button is not found!")
        new_x, new_y = 296, 940
    pyautogui.click(new_x, new_y, duration=1)
    count = 1
    for e in data:
        try:
            if "lang" in e:
                if e["lang"]=="python":
                    continue
            if len(e["query"])>=2000:
                continue
            prompt = e["query"]
            text_id = str(string_to_id(prompt))
            if checkid(text_id):
                continue
            text = input_prompt(prompt)
            print(count)
            count = count + 1
            if count%20==0:
                res = change_ip()
                print(res)
                driver.close()
                time.sleep(5)
                driver = webdriver.Chrome(service=service,options=chrome_options)
                driver.implicitly_wait(2)
                driver.maximize_window()
                driver.get(url)
                enter_proxy_auth()
                time.sleep(5)
            if text is False:
                print(text_id,False)
                pyautogui.click(new_x, new_y, duration=1)
                continue
            now = datetime.now()
            insert_logs(text_id,prompt,text,'Copilot',name,now)
            pyautogui.click(new_x, new_y, duration=1)
        except:
            time.sleep(120)
            continue
        