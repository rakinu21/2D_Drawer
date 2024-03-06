import json
from tkinter import filedialog

class ProjectSaver:
    def __init__(self, canvas):
        self.canvas = canvas

    def save_project(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            shapes = []
            for shape in self.canvas.find_all():
                shape_type = self.canvas.type(shape)
                if shape_type == 'polygon':
                    coords = self.canvas.coords(shape)
                    fill_color = self.canvas.itemcget(shape, 'fill')
                    if len(coords) == 12:  # Hexagon has 6 points (12 coordinates)
                        shapes.append({'type': 'Hexagon', 'coords': coords, 'fill_color': fill_color})
                    else:
                        shapes.append({'type': 'Triangle', 'coords': coords, 'fill_color': fill_color})
                elif shape_type == 'oval':
                    coords = self.canvas.coords(shape)
                    fill_color = self.canvas.itemcget(shape, 'fill')
                    shapes.append({'type': 'Circle', 'coords': coords, 'fill_color': fill_color})
                elif shape_type == 'rectangle':
                    coords = self.canvas.coords(shape)
                    fill_color = self.canvas.itemcget(shape, 'fill')
                    shapes.append({'type': 'Square', 'coords': coords, 'fill_color': fill_color})
            
            with open(file_path, 'w') as file:
                json.dump(shapes, file)