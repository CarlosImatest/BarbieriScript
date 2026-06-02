#barbieri dimensions x = 996 y = 623 (300mm x 185mm) (11.81in x 7.38in)
#9.25x7.75 printable area inch (234.95x196.85 mm) (780.90x653.55 barbieri units)
#10x8 (7.91)in film strip (254x203.2 mm) (843x674 barbieri units)
#1in = 84.32 barbieri units

import cv2
import tkinter as tk

class LoadImage:
    CANVAS_W = 996
    OFFSET = 10
    BARBIERI_UNITS_PER_INCH = 84.32

    def __init__(self, path, film_w, film_h, active_w, active_h):
        self.film_w = film_w * self.BARBIERI_UNITS_PER_INCH
        self.film_h = film_h * self.BARBIERI_UNITS_PER_INCH
        self.active_w = active_w * self.BARBIERI_UNITS_PER_INCH
        self.active_h = active_h * self.BARBIERI_UNITS_PER_INCH
        self.path = path
        self.x_cordinates = []
        self.y_cordinates = []
        self.resized_img = None
        self.clean_img = None  # Clean copy for redrawing after undo

    def redraw(self):
        """Redraw all current points on a fresh copy of the clean image."""
        self.resized_img = self.clean_img.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        for i in range(len(self.x_cordinates)):
            # Reverse the transform to get back to pixel coordinates
            px = self.CANVAS_W - self.x_cordinates[i] + self.OFFSET
            py = self.y_cordinates[i]
            cv2.circle(self.resized_img, (px, py), 5, (0, 0, 255), -1)
            cv2.putText(self.resized_img, f'{self.x_cordinates[i]},{py}',
                        (px + 10, py), font, 0.5, (255, 255, 0), 1)
        cv2.imshow('Image Viewer', self.resized_img)

    def click_event(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x_cordinates.append(self.CANVAS_W - x + self.OFFSET)
            self.y_cordinates.append(y)
            self.redraw()

    def on_ctrl_z(self):
        if self.x_cordinates:
            self.x_cordinates.pop()
            self.y_cordinates.pop()
            print(f"[Undo] Removed last point. {len(self.x_cordinates)} point(s) remaining.")
            self.redraw()
        else:
            print("[Undo] Nothing to undo.")

    def loadImage(self):
        img = cv2.imread(self.path)
        if img is None:
            print(f"Image not found at path: {self.path}")
            return

        h, w = img.shape[:2]
        scale = min(self.film_w / w, self.film_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        top_padding   = int((self.film_h - self.active_h) / 2)
        bot_padding   = int((self.film_h - self.active_h) / 2)
        left_padding  = int((self.film_w - self.active_w) / 2)
        right_padding = int((self.film_w - self.active_w) / 2)

        bordered = cv2.copyMakeBorder(resized, top_padding, bot_padding,
                                      right_padding, left_padding,
                                      cv2.BORDER_CONSTANT, value=[0, 0, 0])

        self.clean_img = bordered
        self.resized_img = bordered.copy()

        cv2.namedWindow('Image Viewer')
        cv2.setMouseCallback('Image Viewer', self.click_event)

        print("Click to add points. Ctrl+Z to undo. Press Esc or Q to finish.")
        cv2.imshow('Image Viewer', self.resized_img)

        # ── Key loop ──────────────────────────────────────────────────────────
        ctrl_held = False
        while True:
            key = cv2.waitKey(20) & 0xFF

            # Exit if window was closed with the X button
            if cv2.getWindowProperty('Image Viewer', cv2.WND_PROP_VISIBLE) < 1:
                break

            if key == 26:           # Ctrl+Z (ASCII 26 = ^Z)
                self.on_ctrl_z()
            elif key == 27:         # Esc
                break
            elif key in (ord('q'), ord('Q')):
                break
        # ─────────────────────────────────────────────────────────────────────

        cv2.destroyAllWindows()

        # Post-processing: group clicks into rows
        if not self.x_cordinates:
            return

        counter = 0
        new_x_cordinates = []
        new_y_cordinates = []
        for i in range(len(self.x_cordinates)):
            if i == len(self.x_cordinates) - 1:
                avg = int(sum(self.y_cordinates[counter:]) / (len(self.y_cordinates) - counter))
                new_x_cordinates.append(self.x_cordinates[counter:i + 1])
                new_y_cordinates.append(avg)
            elif self.y_cordinates[i] * 1.1 < self.y_cordinates[i + 1]:
                avg = int(sum(self.y_cordinates[counter:i + 1]) / (i + 1 - counter))
                new_x_cordinates.append(self.x_cordinates[counter:i + 1])
                new_y_cordinates.append(avg)
                counter = i + 1

        self.x_cordinates = new_x_cordinates
        self.y_cordinates = new_y_cordinates

    def promtFilmSize(self):
        win = tk.Tk()
        win.title("Film Size Input")
        win.resizable(False, False)