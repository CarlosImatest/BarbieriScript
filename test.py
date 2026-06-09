import pygetwindow as gw
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

win = gw.getWindowsWithTitle('Gateway')[0] # Replace with your window title
if win.title == 'Gateway':
    print("Window found!")
