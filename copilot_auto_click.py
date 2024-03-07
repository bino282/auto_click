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
        print('ok')
        # cv2.rectangle(orig_img, (x, y), (x + w, y + h), (0,0,255), 4)
        rx = int(x + w/2)
        ry = int(y + h/2)
        break
    return rx, ry

def input_prompt(prompt):
    # pyautogui.moveTo(settings.copilot_x, settings.copilot_y, duration = 1)
    enter_x, enter_y = find_button_location("./icons/enter.jpg",THRESHOLD=0.9)
    pyautogui.click(enter_x, enter_y)
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
    pyautogui.scroll(-1000)
    while(True):
        time.sleep(5)
        status_x , status_y = find_button_location("./icons/status.jpg")
        if status_x == 0 and status_y == 0:
            break
        pyautogui.scroll(-1000)
    copy_x, copy_y = find_button_location("icons/co_option.jpg")
    if copy_x == 0 and copy_y == 0:
        print("copy button is not found!")
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
    with open("data/Evol-Instruction-66k.json","r",encoding="utf-8") as fr:
        data = json.load(fr)
    random.shuffle(data)
    new_x, new_y = find_button_location("./icons/new.jpg",THRESHOLD=0.7)
    # new_x, new_y = settings.copilot_x, settings.copilot_y
    if new_x==0 and new_y==0:
        print("new button is not found")
        exit()
    pyautogui.click(new_x, new_y, duration=1)
    for e in data:
        prompt = e["instruction"]
        text_id = str(string_to_id(prompt))
        # if f"{text_id}.json" in results_list:
        #     continue
        if checkid(text_id):
            continue
        text = input_prompt(prompt)
        if text is False:
            pyautogui.click(new_x, new_y, duration=1)
            continue
        # with open(f"./data/Evol-Instruction-66k/{text_id}.json","w",encoding="utf-8") as fw:
        #     json.dump({"input": prompt,"output": text}, fw, indent=4 , ensure_ascii=False)
        now = datetime.now()
        insert_logs(text_id,prompt,text,'Copilot','Evol-Instruction',now)
        pyautogui.click(new_x, new_y, duration=1)
