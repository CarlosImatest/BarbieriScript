import tkinter as tk
from tkinter import messagebox

win = tk.Tk()
win.title("Film Size Input")
win.resizable(False, False)

result = {}

# ---------------- HEADER ----------------
header = tk.Label(
    win,
    text="All measurements in Inches",
    font=("Arial", 10, "italic"),
    fg="blue"
)
header.grid(row=0, column=0, columnspan=2, padx=12, pady=(10, 2))

# ---------------- INPUT FIELDS ----------------
fields = [
    ("Width",         "width"),
    ("Height",        "height"),
    ("Active Width",  "active_width"),
    ("Active Height", "active_height")
]

entries = {}

for i, (label_text, key) in enumerate(fields):
    tk.Label(win, text=label_text).grid(
        row=i + 1,
        column=0,
        padx=12,
        pady=6,
        sticky="w"
    )

    entry = tk.Entry(win, width=25)
    entry.grid(row=i + 1, column=1, padx=12, pady=6)

    entries[key] = entry

# ---------------- RADIO BUTTONS ----------------
header2 = tk.Label(
    win,
    text="Use SVG file?",
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

# ---------------- SUBMIT FUNCTION ----------------
def on_submit():
    try:
        result["width"] = float(entries["width"].get().strip())
        result["height"] = float(entries["height"].get().strip())
        result["active_width"] = float(entries["active_width"].get().strip())
        result["active_height"] = float(entries["active_height"].get().strip())

        # Save radio button selection
        result["use_svg"] = svg_choice.get()

        win.destroy()

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter numeric values only."
        )

# ---------------- OK BUTTON ----------------
tk.Button(
    win,
    text="OK",
    width=15,
    command=on_submit
).grid(
    row=len(fields) + 3,
    column=0,
    columnspan=2,
    pady=12
)

win.mainloop()

print("Result:", result)