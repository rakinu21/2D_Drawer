from tkinter import Canvas
from tkinter import colorchooser
from edit.resize import ResizeHandler

from golbal import Global
from shapes.colors import Shape

class CircleDrawer(Shape, ResizeHandler):
    def __init__(self, canvas):
       Shape.__init__(self, canvas)
       ResizeHandler.__init__(self, canvas, self.selected_shape)

    def draw_shape(self, event):
        self.x0, self.y0 = event.x, event.y
        self.selected_shape = self.canvas.create_oval(self.x0, self.y0, self.x0, self.y0, fill="green")
        Global.shape = self
        Global.resize = self
        Global.move_and_zome = self
        self.canvas.tag_bind(self.selected_shape, '<Button-1>',Shape(self.canvas).shape_click)
        self.canvas.bind('<B1-Motion>', lambda event: self.draw_circle(event, self.x0, self.y0))

    def draw_circle(self, event, x0, y0):
        if self.selected_shape:
            x1, y1 = event.x, event.y
            width = abs(x1 - x0)
            height = abs(y1 - y0)
            x_center = (x0 + x1) / 2
            y_center = (y0 + y1) / 2
            radius = min(width, height) / 2
            self.canvas.coords(self.selected_shape, x_center - radius, y_center - radius, x_center + radius, y_center + radius)
            
    def change_color(self):
        color = colorchooser.askcolor()
        if color:
            self.canvas.itemconfig(self.selected_shape, fill=color[1])

