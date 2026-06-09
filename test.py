import pygetwindow as gw
from pynput.keyboard import Key, Controller
import time
import pyautogui as py
import win32gui
import win32con

keyboard = Controller()

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

if py.locateAllOnScreen(r"Images\calibration_acknowledgement.PNG", confidence=90):
    ok_button_done_calibration = py.locateOnScreen(r"Images\ok_button_calibration_done.PNG", confidence=0.90)
    x_ok_button_done_calibration_center = (ok_button_done_calibration[0] + ok_button_done_calibration[2]//2)
    y_ok_button_done_calibration_center = (ok_button_done_calibration[1] + ok_button_done_calibration[3]//2)
    py.moveTo(x_ok_button_done_calibration_center, y_ok_button_done_calibration_center)
    py.click(clicks=1)
    wait_for_mouse()

    if py.locateAllOnScreen(r"Images\calibration_done_ack.PNG", confidence=90):
        ok_button_done_calibration = py.locateOnScreen(r"Images\ok_button_calibration_done.PNG", confidence=0.90)
        x_ok_button_done_calibration_center = (ok_button_done_calibration[0] + ok_button_done_calibration[2]//2)
        y_ok_button_done_calibration_center = (ok_button_done_calibration[1] + ok_button_done_calibration[3]//2)
        py.moveTo(x_ok_button_done_calibration_center, y_ok_button_done_calibration_center)
        py.click(clicks=1)
