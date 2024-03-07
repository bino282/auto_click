import pyautogui
import time
import settings
from browser import open_incognito
from PIL import ImageGrab, Image
import cv2
import numpy as np
import pyperclip
from sql_cli import *

pyautogui.FAILSAFE = False

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
    THRESHOLD = 0.6
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
    pyautogui.moveTo(settings.chat_x, settings.chat_y, duration = 1)
    pyautogui.click(settings.chat_x, settings.chat_y)
    with pyautogui.hold('ctrl'):
        pyautogui.press('a')
    pyautogui.press('delete')
    pyperclip.copy(prompt)
    
    with pyautogui.hold('ctrl'):
        pyautogui.press(['v'])
    # prompt_list = prompt.split("\n")
    # for e in prompt_list:
    #     if e=="":
    #         with pyautogui.hold('shift'):
    #             pyautogui.press(['enter'])
    #     else:
    #         pyautogui.typewrite(e)
    #         with pyautogui.hold('shift'):
    #             pyautogui.press(['enter'])
    pyautogui.typewrite(['enter'])
    pyautogui.moveTo(settings.b_x, settings.b_y, duration = 1)
    pyautogui.click(settings.b_x, settings.b_y)
    # button_img = cv2.imread('icons/enter.jpg', cv2.IMREAD_GRAYSCALE)
    # enter_x, enter_y = find_button_location(cv2_img, button_img)
    # if copy_x == 0 and copy_y == 0:
    #     print("can't find enter btn")
    #     return False
    # pyautogui.click(enter_x, enter_y, duration=1)
    # w8 response
    time.sleep(30)
    # sroll down
    pyautogui.scroll(-5000)
    time_check = 0
    while(1):
        time_check = time_check + 1
        if (time_check>10):
            return False
        else:
            option_x, option_y = find_button_location("./icons/option.jpg")
            if option_x == 0 and option_y == 0:
                time.sleep(5)
                pyautogui.scroll(-5000)
            else:
                break
    
    if option_x == 0 and option_y == 0:
        print("can't find option btn")
        return False
    pyautogui.click(option_x+14, option_y, duration=1)
    copy_x, copy_y = find_button_location("./icons/saochep.jpg")
    if copy_x == 0 and  copy_y== 0:
        print("can't find copy btn")
        return False
    pyperclip.copy(' ')
    pyautogui.moveTo(copy_x, copy_y, duration = 1)
    pyautogui.click(copy_x, copy_y, duration=1)
    time.sleep(5)
    text = pyperclip.paste()
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
        if conv_id in result_list:
            continue
        skip = False
        for e in human_prompt_list[0:4]:
            text = input_prompt(e)
            if text is False:
                skip = True
                break
            if len(text.split())<20:
                skip = True
                break
            messages.append({"from":"human","value":e})
            messages.append({"from":"gpt","value":text})
        if (skip):
            continue
        with open(f"data/conv/{conv_id}.json","w",encoding="utf-8") as fw:
            json.dump({"items":messages, "model":"Gemini Ultra"},fw, indent=4, ensure_ascii=False)
        pyautogui.moveTo(settings.new_chat_x, settings.new_chat_y, duration = 1)
        pyautogui.click(settings.new_chat_x, settings.new_chat_y)
