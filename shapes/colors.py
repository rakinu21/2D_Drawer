from tkinter import colorchooser

class Shape:
    def __init__(self, canvas):
        self.canvas = canvas
        self.selected_shape = None
        self.x0, self.y0 = None, None
        
    def change_color(self):
        color = colorchooser.askcolor()
        if color:
            self.canvas.itemconfig(self.selected_shape, fill=color[1])

    def shape_click(self, event):
        self.selected_shape = event.widget.find_closest(event.x, event.y)
        self.change_color()    