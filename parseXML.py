import json

from lxml import etree
from tkinter import simpledialog, filedialog

class parseXML:
    # offset_x = 0
    # offset_y = 0
    INCH_TO_PX = 96
    INCH_TO_BARBIERI_UNIT= 84.32
    CANVAS_W= 996

    def __init__(self, film_w, film_h, active_w, active_h, path, use_xml):
        self.offset_x = ((film_w - active_w)/2) * self.INCH_TO_PX #convert inch to pixel
        self.offset_y = ((film_h - active_h)/2) * self.INCH_TO_PX
        self.path = path
        self.use_xml = use_xml

    def openXML(self):
        tree = etree.parse(self.path)
        root = tree.getroot()
        self.parseIt(root)

    def parseIt(self, root):

        patch_map = {}

        for elem in root.iter():
            if elem.attrib["id"].startswith("patch"):
                temp = elem.attrib["points"].split(" ")
                patch_map[elem.attrib["id"]] = temp[:len(temp)-2]  # Exclude the last empty string and closing point

        for patch_id, points in patch_map.items():
            temp = points
            counter = 0
            for i in points:
                x, y = i.split(",")
                temp[counter] = [float(x)*0.96 + self.offset_x, float(y)*0.96 + self.offset_y]
                counter += 1
            counter = 0

        center_patch = {}
        for patch_id, points in patch_map.items():
            x_center = self.CANVAS_W - int(((points[0][0] + points[2][0]) / 2)/self.INCH_TO_PX*self.INCH_TO_BARBIERI_UNIT) #converintg from px to barbieri units
            y_center = int(((points[0][1] + points[1][1]) / 2)/self.INCH_TO_PX*self.INCH_TO_BARBIERI_UNIT) #converintg from px to barbieri units
            patch_map[patch_id] = [x_center, y_center]
        
        print(self.offset_x, self.offset_y)
           
        self.saveFile(patch_map)

    def saveFile(self, patch_map):
        patch_map["use_xml"] = self.use_xml
        file_name = simpledialog.askstring("Save File", "Enter a name for the file:")

        if not file_name:
            print("No file name provided. Exiting.")
            exit()
        else:
            with open(f"Film_Coordinates\{file_name}.json", "w") as f:
                json.dump(patch_map, f)