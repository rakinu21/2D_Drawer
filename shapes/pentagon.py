from edit.resize import ResizeHandler
from golbal import Global
from tkinter import Canvas
from tkinter import colorchooser
from shapes.colors import Shape
import math

class PentagonDrawer(Shape, ResizeHandler):

    def __init__(self, canvas):
        Shape.__init__(self, canvas)
        ResizeHandler.__init__(self, canvas, self.selected_shape)

    def draw_shape(self, event):
        self.x0, self.y0 = event.x, event.y
        self.selected_shape = self.canvas.create_polygon(self.x0, self.y0, self.x0, self.y0, self.x0, self.y0, self.x0, self.y0, self.x0, self.y0, fill="yellow")
        Global.shape = self
        Global.resize = self
        Global.move_and_zome = self
        self.canvas.tag_bind(self.selected_shape, '<Button-1>',Shape(self.canvas).shape_click )
        self.canvas.bind('<B1-Motion>', lambda event: self.draw_pentagon(event, self.x0, self.y0))

    def draw_pentagon(self, event, x0, y0):
        if self.selected_shape:
            x1, y1 = event.x, event.y
            side_length = max(abs(x1 - x0), abs(y1 - y0))
            angle = 360 / 5  # Angle for pentagon
            points = []
            for i in range(5):
                angle_rad = math.radians(angle * i - 90)  # Rotate by 90 degrees to make it start from top
                x = x0 + side_length * math.cos(angle_rad)
                y = y0 + side_length * math.sin(angle_rad)
                points.extend([x, y])
            self.canvas.coords(self.selected_shape, *points)

  