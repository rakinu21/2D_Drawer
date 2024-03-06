import json
from tkinter import filedialog

class ProjectOpener:
    def __init__(self, canvas):
        self.canvas = canvas

    def open_project(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                shapes = json.load(file)
                for shape in shapes:
                    shape_type = shape['type']
                    if shape_type == 'Triangle':
                        self.canvas.create_polygon(shape['coords'], fill=shape['fill_color'])
                    elif shape_type == 'Circle':
                        self.canvas.create_oval(shape['coords'], fill=shape['fill_color'])
                    elif shape_type == 'Square':
                        self.canvas.create_rectangle(shape['coords'], fill=shape['fill_color'])
                    elif shape_type == 'Hexagon':
                        self.canvas.create_polygon(shape['coords'], fill=shape['fill_color'])
