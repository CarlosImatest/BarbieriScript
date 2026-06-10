from LoadImage import *
from barbieri import *
from parseXML import *
import json
import tkinter as tk
from tkinter import simpledialog, filedialog

def film_size_input_window():
    win = tk.Tk()
    win.title("Film Size Input")
    win.resizable(False, False)
    result = {}

    # label header for the fields
    header = tk.Label(win, text="All measurements in Inches", font=("Arial", 10, "italic"), fg="blue")
    header.grid(row=0, column=0, columnspan=2, padx=12, pady=(10, 2))

    #fields for film size input
    fields = [
        ("Width",         "width"),
        ("Height",        "height"),
        ("Active Width",  "active_width"),
        ("Active Height", "active_height")
    ]

    entries = {}

    # creating the labels and entries (starting from row 1 because header is row 0)
    for i, (label_text, key) in enumerate(fields):
        tk.Label(win, text=label_text).grid(row=i+1, column=0, padx=12, pady=6, sticky="w")
        entry = tk.Entry(win, width=25)
        entry.grid(row=i+1, column=1, padx=12, pady=6)
        entries[key] = entry

    def on_submit():
        try:
            # Save each input to the result dictionary
            result["width"]         = float(entries["width"].get().strip())
            result["height"]        = float(entries["height"].get().strip())
            result["active_width"]  = float(entries["active_width"].get().strip())
            result["active_height"] = float(entries["active_height"].get().strip())

            result["use_xml"] = svg_choice.get() == "Yes"  # Convert to boolean
            win.destroy()
        except ValueError:
            from tkinter import messagebox
            messagebox.showerror("Input Error", "Please enter numeric values only.")
    
    # ---------------- RADIO BUTTONS ----------------
    header2 = tk.Label(
        win,
        text="Use XML file?",
        font=("Arial", 10, "italic"),
        fg="blue"
    )
    header2.grid(
        row=len(fields) + 1,
        column=0,
        columnspan=2,
        padx=12,
        pady=(2, 10)
    )

    # Variable that stores Yes/No selection
    svg_choice = tk.StringVar(value="No")

    # Radio buttons
    tk.Radiobutton(
        win,
        text="Yes",
        variable=svg_choice,
        value="Yes"
    ).grid(row=len(fields) + 2, column=0, pady=4)

    tk.Radiobutton(
        win,
        text="No",
        variable=svg_choice,
        value="No"
    ).grid(row=len(fields) + 2, column=1, pady=4)


    # 3. Create the button at the bottom
    tk.Button(win, text="OK", width=10, command=on_submit).grid(
        row=len(fields) + 3, column=0, columnspan=2, pady=12
    )

    win.mainloop()
    return result

def pick_image_path():
    root = tk.Tk()
    root.withdraw()  # hide the empty window
    path = filedialog.askopenfilename(
        title="Select A File",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.tiff *.bmp *.svg"),
            ("All files",   "*.*")
        ]
    )
    root.destroy()
    return path  # returns "" if the user cancels

# Main execution
# Get film size input from the user
x, y, x_active, y_active, use_xml = film_size_input_window().values()

print(not use_xml)
if not use_xml:
    # get image path from the user
    path = pick_image_path()
    if not path:
        print("No file selected. Exiting.")
        exit()

    # loading image
    img = LoadImage(path, x, y, x_active, y_active, use_xml)
    img.loadImage()
    # getting the x and y coordinates of the patches from img
    x_coordinate = img.x_cordinates
    y_coordinate = img.y_cordinates
    xml_coordinates = img.new_format_dict

    # window asking for a filename
    root = tk.Tk()
    root.withdraw()  # hide the empty main window

    file_name = simpledialog.askstring("Save File", "Enter a name for the file:")
    root.destroy()

    if not file_name:
        print("No file name provided. Exiting.")
        exit()
    else:
        with open(f"Film_Coordinates\{file_name}.json", "w") as f:
            json.dump(xml_coordinates, f)
else:
    path = pick_image_path()
    if not path:
        print("No file selected. Exiting.")
        exit()
    
    test1 = parseXML(x, y, x_active, y_active, path, use_xml)
    test1.openXML()

    