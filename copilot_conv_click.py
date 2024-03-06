import pyautogui
pyautogui.FAILSAFE = False
import time
import settings
import cv2
import numpy as np
import pyperclip
from sql_cli import *



# find copy button
# all img must be grayscale

def find_button_location(button_img_path):
    # take screenshot
    img = pyautogui.screenshot()
    
    # find copy btn location
        
    screen_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    button_img = cv2.imread(button_img_path, cv2.IMREAD_GRAYSCALE)
    w_img, h_img = screen_img.shape[1], screen_img.shape[0]
    w, h = button_img.shape[1], button_img.shape[0]
    result = cv2.matchTemplate(screen_img, button_img, cv2.TM_CCOEFF_NORMED)
    THRESHOLD = 0.8
    loc = np.where(result >= THRESHOLD)
    rx, ry = 0, 0
    #Draw boudning box
    for y, x in zip(loc[0], loc[1]):
        print('ok')
        # cv2.rectangle(orig_img, (x, y), (x + w, y + h), (0,0,255), 4)
        rx = int(x + w/2)
        ry = int(y + h/2)
        break
    return rx, ry

def input_prompt(prompt):
    # pyautogui.moveTo(settings.copilot_x, settings.copilot_y, duration = 1)
    pyautogui.click(settings.copilot_x, settings.copilot_y)
    with pyautogui.hold('ctrl'):
        pyautogui.press('a')
    pyautogui.press('delete')
    pyperclip.copy(prompt)
    
    with pyautogui.hold('ctrl'):
        pyautogui.press(['v'])
    
    pyautogui.typewrite(['enter'])
    pyautogui.click(97,843)
    pyautogui.scroll(-10)
    time.sleep(10)
    pyautogui.scroll(-500)
    check_button = True
    time_check = 0
    while(check_button):
        time_check = time_check + 1
        if (time_check>10):
            return False
        else:
            status_x , status_y = find_button_location("./icons/status.jpg")
            if status_x == 0 and status_y == 0:
                copy_x, copy_y = find_button_location("icons/co_option.jpg")
                if copy_x == 0 and copy_y == 0:
                    time.sleep(5)
                    pyautogui.scroll(-5000)
                else:
                    break
    
    pyperclip.copy(' ')
    pyautogui.click(copy_x-10, copy_y, duration=1)
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
    with open("data/code-gpt4.json","r",encoding="utf-8") as fr:
        data = json.load(fr)
    random.shuffle(data)
    for e in data:
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
        for e in human_prompt_list[0:4]:
            text = input_prompt(e)
            messages.append({"from":"human","value":e})
            messages.append({"from":"gpt","value":text})
        with open(f"data/conv/{conv_id}.json","w",encoding="utf-8") as fw:
            json.dump(messages,fw, indent=4, ensure_ascii=False)
        pyautogui.click(230, 959, duration=1)
