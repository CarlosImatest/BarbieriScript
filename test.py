import pyautogui as py
from win32gui import GetCursorInfo
import win32gui
import win32con
import win32api
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

gray_patch_x, gray_patch_y = [[670, 604, 538, 472], [736, 670, 604, 538, 472, 406], [802, 736, 406, 340], [802, 736, 406, 340], [802, 736, 406, 340], [802, 736, 406, 340], [736, 670, 604, 538, 472, 406], [670, 604, 538, 472]], [48+(i*66) for i in range(8)]
color_patch_x, color_patch_y = [i*20 for i in range(1,8) if i%2!=0], [i*20 for i in range(1,8) if i%2!=0]



time.sleep(2)


def wait_for_mouse():
    # Fetch the ACTUAL handles currently assigned by Windows
    # IDC_WAIT is the spinning circle (32512)
    # IDC_APPSTARTING is the arrow + circle (32515)
    busy_handle = win32gui.LoadCursor(0, win32con.IDC_WAIT)
    starting_handle = win32gui.LoadCursor(0, win32con.IDC_APPSTARTING)
    
    busy_handles = [busy_handle, starting_handle]
    
    # Give the app a split second to actually trigger the busy state
    time.sleep(0.2) 
    
    while True:
        info = win32gui.GetCursorInfo()
        current_handle = info[1]
        
        if current_handle in busy_handles:
            time.sleep(0.5)
        else:
            # The cursor is no longer in a busy state
            break

x_pos = py.locateOnScreen(r"Images\x_pos.PNG", confidence=0.90)
y_pos = py.locateOnScreen(r"Images\y_pos.PNG", confidence=0.90)
x_measure = py.locateOnScreen(r"Images\Measure_button.PNG", confidence=0.90)
x_pos_center = (x_pos[0] + x_pos[2]//2)+60
x_pos_y_center = x_pos[1] + x_pos[3]//2
y_pos_x_center = (y_pos[0] + y_pos[2]//2)+60
y_pos_y_center = y_pos[1] + y_pos[3]//2
x_measure_center = (x_measure[0] + x_measure[2]//2)
y_measure_center = (x_measure[1] + x_measure[3]//2)
for i in range(len(gray_patch_x)):
    py.moveTo(y_pos_x_center, y_pos_y_center)
    py.click(clicks=2, interval=0.2)
    keyboard.type(str(gray_patch_y[i]))
    keyboard.press(Key.enter)
    wait_for_mouse()
    
    for j in range(len(gray_patch_x[i])):
        py.moveTo(x_pos_center, x_pos_y_center)
        py.click(clicks=2, interval=0.2)   
        py.moveTo(x_pos_center, x_pos_y_center)
        py.click(clicks=2, interval=0.2)
        keyboard.type(str(gray_patch_x[i][j]))
        keyboard.press(Key.enter)
        wait_for_mouse()

        py.moveTo(x_measure_center, y_measure_center)
        py.click(clicks=1)
        wait_for_mouse()

