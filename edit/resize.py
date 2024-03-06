

import math

class ResizeHandler:
    def __init__(self, canvas, selected_shape):
        self.canvas = canvas
        self.selected_shape = selected_shape
    
    def start_move(self, event):
        if event.num == 3:  # Check if right mouse button is pressed
            item = self.canvas.find_closest(event.x, event.y)
            if item and self.canvas.type(item) in ['rectangle', 'oval', 'polygon']:
                self.selected_shape = item
                self.last_x = event.x
                self.last_y = event.y
                self.canvas.bind('<B3-Motion>', self.move_shape)
                self.canvas.bind('<KeyPress-Up>', self.resize_up)  # Bind up arrow key for resizing up
                self.canvas.bind('<KeyPress-Down>', self.resize_down)  # Bind down arrow key for resizing down

    def resize_up(self, event):
        if self.selected_shape:
            factor = 1.1  # Increase size
            self.resize_shape(factor)

    def resize_down(self, event):
        if self.selected_shape:
            factor = 0.9  # Decrease size
            self.resize_shape(factor)

    def move_shape(self, event):
        if self.selected_shape:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.canvas.move(self.selected_shape, dx, dy)
            self.last_x = event.x
            self.last_y = event.y

    def resize_shape(self, event):
        if self.selected_shape:
            current_coords = self.canvas.coords(self.selected_shape)
            if event.keysym == "Up":
                factor = 1.1  # Increase size
                self.resize_shape_coords(current_coords, factor)
            elif event.keysym == "Down":
                factor = 0.9  # Decrease size
                self.resize_shape_coords(current_coords, factor)
            elif event.keysym == "Left":
               self.rotate_shape(-1)  # Rotate left by 10 degrees
            elif event.keysym == "Right":
               self.rotate_shape(1)  # Rotate right by 10 degrees


    def resize_shape_coords(self, coords, factor):
        # Calculate center of the shape
        x_center = (coords[0] + coords[2]) / 2
        y_center = (coords[1] + coords[3]) / 2

        # Resize shape around its center
        new_coords = []
        for i in range(len(coords)):
            if i % 2 == 0:
                new_coords.append(x_center + (coords[i] - x_center) * factor)
            else:
                new_coords.append(y_center + (coords[i] - y_center) * factor)

        self.canvas.coords(self.selected_shape, *new_coords)


    def rotate_shape(self, angle):
        if self.selected_shape:
            # Get current coordinates
            coords = self.canvas.coords(self.selected_shape)
            # Calculate center of the shape
            x_center = (coords[0] + coords[2]) / 2
            y_center = (coords[1] + coords[3]) / 2
            # Rotate each point around the center
            rotated_coords = []
            for i in range(0, len(coords), 2):
                x = coords[i]
                y = coords[i + 1]
                # Translate to origin
                x -= x_center
                y -= y_center
                # Perform rotation
                new_x = x * math.cos(math.radians(angle)) - y * math.sin(math.radians(angle))
                new_y = x * math.sin(math.radians(angle)) + y * math.cos(math.radians(angle))
                # Translate back
                new_x += x_center
                new_y += y_center
                rotated_coords.extend([new_x, new_y])
            self.canvas.coords(self.selected_shape, *rotated_coords)
