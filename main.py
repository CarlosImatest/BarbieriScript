#x is 0-996 y is 0-623
#film UHDR 8x10"
#color patch .517h x .31w inches, 13.123h x 7.874w mm
#square patch .763x.763 inches, 19.39x19.39mm
#heads moves 60 in y when you click the measure button
#47mm from edge to the first patch (161barbieri units)

import time

from pynput.keyboard import Controller
from barbieri import barbieri
import json
from tkinter import filedialog
import tkinter as tk
import pygetwindow as gw

def file_path():
    root = tk.Tk()
    root.withdraw()  # hide the empty window
    path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[
            ("All files",   "*.*")
        ]
    )
    root.destroy()
    return path  # returns "" if the user cancels


keyboard = Controller()

path = file_path()
try:
    with open(path, "r") as f:
        grid = json.load(f)
        use_xml = grid.pop("use_xml") #get the last item in the dict which is the use_xml bool and remove it from the dict so we are left with only the patch coordinates in grid
        # if use_xml:
        #     barbieri_instance = barbieri(grid, use_xml)

except FileNotFoundError:
    print("File not found.")
    exit()
    
time.sleep(1) #give the user a moment to close the file dialog before we try to find the window
# Find the window by its title
try:
    win = gw.getWindowsWithTitle('Gateway')[0] # Replace with your window title
    if win.isMinimized:
        win.restore()
    win.activate()
except IndexError:
    print("Window not found")

barbieri_instance = barbieri(grid, use_xml)
barbieri_instance.start_measurement()



