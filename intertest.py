import json

from lxml import etree
from tkinter import simpledialog, filedialog

# tree = etree.parse(r"Images\ITUHDR36_L1_Test.svg")
# root = tree.getroot()

# start_id = 1477
# step = 8
# count = 36

# id_map = {}

# # Build mapping
# for i in range(count):
#     old_id = f"polyline{start_id + i * step}"
#     new_id = f"patch{i+1:02d}"   # patch01, patch02, ...

#     id_map[old_id] = new_id


# # Apply mapping
# for elem in root.iter():
#     old = elem.attrib.get("id")

#     if old in id_map:
#         elem.attrib["id"] = id_map[old]


# tree.write(
#     "renamed.svg",
#     pretty_print=True,
#     xml_declaration=True,
#     encoding="utf-8"
# )

offset_x = 36
offset_y = 12
inch_to_px = 96
inch_to_barbieri_unit = 84.32
canvas_w = 996

tree = etree.parse(r"renamed.svg")
root = tree.getroot()

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
        temp[counter] = [float(x)*0.96 + offset_x, float(y)*0.96 + offset_y]
        counter += 1
    counter = 0

center_patch = {}
for patch_id, points in patch_map.items():
    x_center = canvas_w - int(((points[0][0] + points[2][0]) / 2)/inch_to_px*inch_to_barbieri_unit) #converintg from px to barbieri units
    y_center = int(((points[0][1] + points[1][1]) / 2)/inch_to_px*inch_to_barbieri_unit) #converintg from px to barbieri units
    patch_map[patch_id] = [x_center, y_center]

# for patch_id, points in patch_map.items():
#     print(f"{patch_id}: {points}")


file_name = simpledialog.askstring("Save File", "Enter a name for the file:")
#root.destroy()

if not file_name:
    print("No file name provided. Exiting.")
    exit()
else:
    with open(f"Film_Coordinates\{file_name}.json", "w") as f:
        json.dump(patch_map, f)