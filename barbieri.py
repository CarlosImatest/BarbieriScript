from logging import root
from tkinter import messagebox, simpledialog, Tk
import pyautogui as py
from win32gui import GetCursorInfo
import win32gui
import win32con
from pynput.keyboard import Key, Controller, Listener
import time
import pygetwindow as gw



class barbieri:
    OFFSET_Y = 60 # head moves 60 in y when measuring
    #constructor
    def __init__(self, grid, use_xml):
        self.grid = grid
        self.keyboard = Controller()
        self.paused = False
        self._start_listener()
        self.x_pos = py.locateOnScreen(r"Images\x_pos.PNG", confidence=0.90)
        self.y_pos = py.locateOnScreen(r"Images\y_pos.PNG", confidence=0.90)
        self.calibration_button = py.locateOnScreen(r"Images\Absolute_button.PNG", confidence=0.85)
        self.x_measure = py.locateOnScreen(r"Images\Measure_button.PNG", confidence=0.90)
        
        self.x_pos_center = (self.x_pos[0] + self.x_pos[2]//2)+60 #offset by 60 when measuring
        self.x_pos_y_center = self.x_pos[1] + self.x_pos[3]//2
        self.y_pos_x_center = (self.y_pos[0] + self.y_pos[2]//2)+60 #offset by 60 when measuring
        self.y_pos_y_center = self.y_pos[1] + self.y_pos[3]//2
        self.x_measure_center = (self.x_measure[0] + self.x_measure[2]//2)
        self.y_measure_center = (self.x_measure[1] + self.x_measure[3]//2)
        self.x_calibration_button_center = (self.calibration_button[0] + self.calibration_button[2]//2)
        self.y_calibration_button_center = (self.calibration_button[1] + self.calibration_button[3]//2)

        self.use_xml = use_xml

        self.root = Tk()


    def _start_listener(self):
        def on_press(key):
            if key == Key.esc:
                self.paused = not self.paused
                if self.paused:
                    print("\n Paused — press ESC again to resume")
                else:
                    print("Resumed")
        
        # deamon = True means the listener will automatically close when the main program exits
        self._listener = Listener(on_press=on_press)
        self._listener.daemon = True
        self._listener.start()

    def _wait_if_paused(self):
        while self.paused:
            time.sleep(0.1)  # sit idle until unpaused


    def wait_for_mouse(self):
        # Fetch the ACTUAL handles currently assigned by Windows
        # IDC_WAIT is the spinning circle (32512)
        # IDC_APPSTARTING is the arrow + circle (32515)
        busy_handle = win32gui.LoadCursor(0, win32con.IDC_WAIT)
        starting_handle = win32gui.LoadCursor(0, win32con.IDC_APPSTARTING)
        
        busy_handles = [busy_handle, starting_handle]
        
        # Give the app a split second to actually trigger the busy state
        time.sleep(0.2) 
        
        while True:
            self._wait_if_paused()  # Check if we should be paused before checking the cursor
            info = win32gui.GetCursorInfo()
            current_handle = info[1]
            
            if current_handle in busy_handles:
                time.sleep(0.5)
            else:
                # The cursor is no longer in a busy state
                break

    def start_measurement(self):
        time.sleep(2) # give user time to switch to the barbieri app

        if self.use_xml:
            self.start_measurement_xml()
        else:
            self.start_measurement_custom()
    
    def calibrate(self):

        #move x axis to zero to set up for calibration
        py.moveTo(self.x_pos_center, self.x_pos_y_center)
        py.click(clicks=2, interval=0.2)
        self.keyboard.type("25")
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        self.wait_for_mouse()

        #move y axis to zero to set up for calibration
        py.moveTo(self.y_pos_x_center, self.y_pos_y_center)
        py.click(clicks=2, interval=0.2)
        self.keyboard.type("25")
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)
        self.wait_for_mouse()

        #start the calibration
        py.moveTo(self.x_calibration_button_center, self.y_calibration_button_center)
        py.click(clicks=1)
        self.wait_for_mouse()

        ok_button_done_calibration = py.locateOnScreen(r"Images\ok_button_calibration_done.PNG", confidence=0.90)
        x_ok_button_done_calibration_center = (ok_button_done_calibration[0] + ok_button_done_calibration[2]//2)
        y_ok_button_done_calibration_center = (ok_button_done_calibration[1] + ok_button_done_calibration[3]//2)

        win = gw.getWindowsWithTitle('Gateway')[0] # Replace with your window title
        if win.title == 'Gateway':
            win.activate() #bring the window to the foreground after calibration is done
            time.sleep(0.5)
            # keyboard = Controller()
            # keyboard.press(Key.enter)
            # keyboard.release(Key.enter)
            # time.sleep(3) #give the app a moment to register the enter key press before we start the measurements
            # self.wait_for_mouse() #wait for the app to finish any processing it needs to do after calibration before we start measurements
            py.moveTo(x_ok_button_done_calibration_center, y_ok_button_done_calibration_center)
            py.click(clicks=1)
            self.wait_for_mouse() #wait for the app to finish any processing it needs to do

    def move_to_xy(self):
        print("Moving to next patch...")

    def start_measurement_xml(self):
        self.calibrate() #calibrate before starting measurements
        current_y = 0 
        previous_y = 0
        counter = 0

        for patch, xy in self.grid.items():
            current_y = xy[1]
            print(current_y, previous_y)
            if current_y != previous_y: #check if we need to move the y input (only move if the y value has changed since 
                                        #the last patch, otherwise we can skip straight to the x input and measure)
                self._wait_if_paused() #check if we should be paused before starting the next patch
                py.moveTo(self.y_pos_x_center, self.y_pos_y_center)
                time.sleep(0.2) #give a moment for the mouse to move before clicking
                py.click(clicks=2, interval=0.2)
                self.keyboard.type(str(xy[1] - self.OFFSET_Y)) #add offset to y value to account for the head moving down when measuring
                self.keyboard.press(Key.enter)
                self.wait_for_mouse()
                previous_y = current_y

            py.moveTo(self.x_pos_center, self.x_pos_y_center)
            py.click(clicks=2, interval=0.2)   
            py.moveTo(self.x_pos_center, self.x_pos_y_center)
            py.click(clicks=2, interval=0.2)
            self.keyboard.type(str(xy[0]))
            self.keyboard.press(Key.enter)
            self.wait_for_mouse()

            py.moveTo(self.x_measure_center, self.y_measure_center)
            py.click(clicks=1)
            self.wait_for_mouse()
            counter += 1

        self.root.withdraw()
        messagebox.showinfo(title="Measurement Complete", message=f"All {counter} patches have been measured. Click OK to exit.")
        # Clean up the window resource
        self.root.destroy()

    def start_measurement_custom(self):
        self.calibrate() #calibrate before starting measurements
        self.wait_for_mouse() #wait for calibration to finish before starting measurements
        gray_patch_x = self.grid["x"]
        gray_patch_y = self.grid["y"]
        counter = 0

        for i in range(len(gray_patch_y)):
            self._wait_if_paused() #check if we should be paused before starting the next patch
            py.moveTo(self.y_pos_x_center, self.y_pos_y_center)
            time.sleep(0.2) #give a moment for the mouse to move before clicking
            py.click(clicks=2, interval=0.2)
            self.keyboard.type(str(gray_patch_y[i] - self.OFFSET_Y)) #add offset to y value to account for the head moving down when measuring
            self.keyboard.press(Key.enter)
            self.wait_for_mouse()

            #inner loop to measure all the patches in the current row before moving to the next row
            for j in range(len(gray_patch_x[i])):
                self._wait_if_paused() #check if we should be paused before starting the next patch
                py.moveTo(self.x_pos_center, self.x_pos_y_center)
                py.click(clicks=2, interval=0.2)   
                py.moveTo(self.x_pos_center, self.x_pos_y_center)
                py.click(clicks=2, interval=0.2)
                self.keyboard.type(str(gray_patch_x[i][j]))
                self.keyboard.press(Key.enter)
                self.wait_for_mouse()

                py.moveTo(self.x_measure_center, self.y_measure_center)
                py.click(clicks=1)
                self.wait_for_mouse()
                counter += 1

        self.root.withdraw()
        messagebox.showinfo(title="Measurement Complete", message=f"All {counter} patches have been measured. Click OK to exit.")
        # Clean up the window resource
        self.root.destroy()


                