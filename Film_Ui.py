import tkinter as tk

class film_ui:
    #constructor that takes in the grid size and builds the grid coordinates
    def __init__(self, col_x, row_y, size=60, margin=10):
        # Build the grid from the integers if needed
        self.col_x = [[802 - (i * 66) for i in range(col_x)] for _ in range(col_x)]
        self.row_y = [108 + (i * 66) for i in range(row_y)]
        self.size = size
        self.margin = margin

    def create_dynamic_film_strip(self):
        root = tk.Tk()
        root.title("Dynamic Film Strip")

        # 1. Calculate required dimensions
        grid_size = len(self.col_x) * (self.size + self.margin) + self.margin

        # 2. Create canvas
        canvas = tk.Canvas(root, width=grid_size, height=grid_size, bg="#222")
        canvas.pack()
        del_cor = []

        # Define the click behavior INSIDE so it can see 'canvas'
        def on_click_del(event):
            # Find the ID of the object currently under the mouse340
            item = canvas.find_withtag("current")
            
            if item:
                # item is a tuple, e.g., (1,)
                # Get the tags associated with the clicked item
                tags = canvas.gettags(item)
                
                # If we tagged the square and text with a unique ID, 
                # we can delete both at once.
                for tag in tags:
                    if tag.startswith("group_"):
                        row = int(tag[tag.find("_")+1:].split('.')[0])
                        col = int(tag[tag.find("_")+1:].split('.')[1])
                        del_cor.append([row,col])  # Store the frame number
                        canvas.delete(tag)

        # 3. Draw the squares
        for r in range(len(self.col_x)):
            for c in range(len(self.col_x)):
                x1 = c * (self.size + self.margin) + self.margin
                y1 = r * (self.size + self.margin) + self.margin
                x2 = x1 + self.size
                y2 = y1 + self.size
                
                frame_num = c + 1
                
                # We give the rectangle and the text the SAME group tag
                # so clicking either deletes the whole "unit"
                group_tag = f"group_{r+1}.{frame_num}"
                
                canvas.create_rectangle(x1, y1, x2, y2, fill="gray", 
                                        outline="white", tags=("square", group_tag))
                
                canvas.create_text(x1 + self.size/2, y1 + self.size/2, text=str(frame_num), 
                                fill="white", tags=("text", group_tag))

        # 4. BIND the click event to the canvas
        # <Button-1> is the Left Mouse Click
        canvas.bind("<Button-1>", on_click_del)

        root.mainloop()
        self.del_array(del_cor, self.col_x)


    def del_array(self, del_arr, col_x):
            new_col_x = col_x.copy()
            for row, col in del_arr:
                new_col_x[row-1][col-1] = 0
            
            new_col_x = [[x for x in row if x != 0] for row in new_col_x]
            self.col_x = new_col_x
            
            print(self.col_x)



# # Your grid logic
# col_x = [[802-(i*66) for i in range(8)] for _ in range(8)]
# row_y = [[108+(i*66) for i in range(8)] for _ in range(8)]

# grid_len = len(col_x)
# create_dynamic_film_strip(grid_len, col_x, row_y)