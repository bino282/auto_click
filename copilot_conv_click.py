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

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
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
    time.sleep(5)
    import random
    result_list = os.listdir("data/conv")
    result_list = [e.split(".")[0] for e in result_list]
    with open("data/code-gpt4.json","r",encoding="utf-8") as fr:
        data = json.load(fr)
    random.shuffle(data)
    url = "https://copilot.microsoft.com/"
    driver.get(url)
    time.sleep(5)
    new_x, new_y = find_button_location("./icons/new.jpg")
    if new_x == 0 and new_y ==0:
        print("new button is not found!")
        new_x, new_y = 296, 940
    pyautogui.click(new_x, new_y, duration=1)
    count = 0
    for e in data:
        count = count + 1
        if count%20==0:
            driver.close()
            driver = webdriver.Chrome(service=service,options=chrome_options)
            driver.implicitly_wait(2)
            driver.maximize_window()
            driver.get(url)
            time.sleep(5)
        items = e["items"]
        human_prompt_list = []
        gpt_answer_list = []
        for i in range(len(items)):
            if items[i]["from"]=="human":
                human_prompt_list.append(items[i]["value"])
            else:
                gpt_answer_list.append(items[i]["value"])
        skip = True
        for a in gpt_answer_list[0:3]:
            if "```" in a:
                skip = False
                break
        if skip:
            continue

        messages = []
        conv_id = str(string_to_id(human_prompt_list[0]))
        if conv_id in result_list:
            continue
        skip = False
        for e in human_prompt_list[0:3]:
            text = input_prompt(e)
            if text is False:
                print(conv_id,False)
                pyautogui.click(new_x, new_y, duration=1)
                skip = True
                break
            messages.append({"from":"human","value":e})
            messages.append({"from":"gpt","value":text})
        if skip:
            continue
        with open(f"data/conv/{conv_id}.json","w",encoding="utf-8") as fw:
            json.dump({"items":messages, "model":"Copilot"},fw, indent=4, ensure_ascii=False)
        pyautogui.click(new_x, new_y, duration=1)