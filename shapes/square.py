from edit.resize import ResizeHandler
from golbal import Global
from tkinter import Canvas
from tkinter import colorchooser
from shapes.colors import Shape

class SquareDrawer(Shape , ResizeHandler):
   
    def __init__(self, canvas):
        Shape.__init__(self, canvas)
        ResizeHandler.__init__(self, canvas, self.selected_shape)

    def draw_shape(self, event):
        self.x0, self.y0 = event.x, event.y
        self.selected_shape = self.canvas.create_rectangle(self.x0, self.y0, self.x0, self.y0, fill="red")
        Global.shape = self
        Global.resize = self
        Global.move_and_zome = self
        self.canvas.tag_bind(self.selected_shape, '<Button-1>',Shape(self.canvas).shape_click)
        self.canvas.bind('<B1-Motion>', lambda event: self.draw_square(event, self.x0, self.y0))

    def draw_square(self, event, x0, y0):
        if self.selected_shape:
            x1, y1 = event.x, event.y
            self.canvas.coords(self.selected_shape, x0, y0, x1, y1)
            
