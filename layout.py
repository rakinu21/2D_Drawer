from tkinter import *
from tkinter import colorchooser, filedialog
import math
import json

def open_project():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            shapes = json.load(file)
            for shape in shapes:
                shape_type = shape['type']
                if shape_type == 'Triangle':
                    canvas.create_polygon(shape['coords'], fill=shape['fill_color'])
                elif shape_type == 'Circle':
                    canvas.create_oval(shape['coords'], fill=shape['fill_color'])
                elif shape_type == 'Square':
                    canvas.create_rectangle(shape['coords'], fill=shape['fill_color'])
                elif shape_type == 'Hexagon':
                    canvas.create_polygon(shape['coords'], fill=shape['fill_color'])

def save_project():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        shapes = []
        for shape in canvas.find_all():
            shape_type = canvas.type(shape)
            if shape_type == 'polygon':
                coords = canvas.coords(shape)
                fill_color = canvas.itemcget(shape, 'fill')
                if len(coords) == 12:  # Hexagon has 6 points (12 coordinates)
                    shapes.append({'type': 'Hexagon', 'coords': coords, 'fill_color': fill_color})
                else:
                    shapes.append({'type': 'Triangle', 'coords': coords, 'fill_color': fill_color})
            elif shape_type == 'oval':
                coords = canvas.coords(shape)
                fill_color = canvas.itemcget(shape, 'fill')
                shapes.append({'type': 'Circle', 'coords': coords, 'fill_color': fill_color})
            elif shape_type == 'rectangle':
                coords = canvas.coords(shape)
                fill_color = canvas.itemcget(shape, 'fill')
                shapes.append({'type': 'Square', 'coords': coords, 'fill_color': fill_color})
        
        with open(file_path, 'w') as file:
            json.dump(shapes, file)

def shape_click(event):
    global selected_shape
    selected_shape = event.widget.find_closest(event.x, event.y)
    change_color()

def draw_shape(shape_type, event):
    global selected_shape, x0, y0
    x0, y0 = event.x, event.y
    if shape_type == 'Hexagon':
        selected_shape = canvas.create_polygon(x0, y0, x0, y0, x0, y0, x0, y0, x0, y0, x0, y0, fill="orange")
        canvas.tag_bind(selected_shape, '<Button-1>', shape_click)
        canvas.bind('<B1-Motion>', lambda event: draw_hexagon(event, x0, y0, selected_shape))
    elif shape_type == 'Circle':
        selected_shape = canvas.create_oval(x0, y0, x0, y0, fill="green")
        canvas.tag_bind(selected_shape, '<Button-1>', shape_click)
        canvas.bind('<B1-Motion>', lambda event:draw_circle(event, x0, y0, selected_shape))
    elif shape_type == 'Square':
        selected_shape = canvas.create_rectangle(x0, y0, x0, y0, fill="red")
        canvas.tag_bind(selected_shape, '<Button-1>', shape_click)
        canvas.bind('<B1-Motion>', lambda event: draw_square(event, x0, y0, selected_shape))
    elif shape_type == 'Triangle':
        selected_shape = canvas.create_polygon(x0, y0, x0, y0, x0, y0, fill="blue")
        canvas.tag_bind(selected_shape, '<Button-1>', shape_click)
        canvas.bind('<B1-Motion>', lambda event: draw_triangle(event, x0, y0, selected_shape))
    elif shape_type == 'Pentagon':
        selected_shape = canvas.create_polygon(x0, y0, x0, y0, x0, y0, x0, y0, x0, y0, fill="yellow")
        canvas.tag_bind(selected_shape, '<Button-1>', shape_click)
        canvas.bind('<B1-Motion>', lambda event: draw_pentagon(event, x0, y0, selected_shape))

  
    canvas.bind('<BackSpace>', lambda event: delete_shape(selected_shape ))


def delete_shape(shape_id ):
    canvas.delete(shape_id)
    

def draw_hexagon(event, x0, y0, selected_shape):
    if selected_shape:
        x1, y1 = event.x, event.y
        side_length = max(abs(x1 - x0), abs(y1 - y0))
        angle = 360 / 6  
        points = []
        for i in range(6):
            angle_rad = math.radians(angle * i)
            x = x0 + side_length * math.cos(angle_rad)
            y = y0 + side_length * math.sin(angle_rad)
            points.extend([x, y])
        canvas.coords(selected_shape, *points)

def draw_circle(event, x0, y0, selected_shape):
    if selected_shape:
        x1, y1 = event.x, event.y
        width = abs(x1 - x0)
        height = abs(y1 - y0)
        x_center = (x0 + x1) / 2
        y_center = (y0 + y1) / 2
        radius = min(width, height) / 2
        canvas.coords(selected_shape, x_center - radius, y_center - radius, x_center + radius, y_center + radius)

def draw_square(event, x0, y0, selected_shape):
    if selected_shape:
        x1, y1 = event.x, event.y
        canvas.coords(selected_shape, x0, y0, x1, y1)


def draw_triangle(event, x0, y0, selected_shape):
    if selected_shape:
        x1, y1 = event.x, event.y
        points = [x0, y0, x1, y1, x1, y0]  # Triangle with base on x-axis
        canvas.coords(selected_shape, *points)

def draw_pentagon(event, x0, y0, selected_shape):
    if selected_shape:
        x1, y1 = event.x, event.y
        side_length = max(abs(x1 - x0), abs(y1 - y0))
        angle = 360 / 5  # Angle for pentagon
        points = []
        for i in range(5):
            angle_rad = math.radians(angle * i - 90)  # Rotate by 90 degrees to make it start from top
            x = x0 + side_length * math.cos(angle_rad)
            y = y0 + side_length * math.sin(angle_rad)
            points.extend([x, y])
        canvas.coords(selected_shape, *points)    


def resize_shape(event):
    global selected_shape
    if selected_shape:
        current_coords = canvas.coords(selected_shape)
        if event.keysym == "Up":
            factor = 1.1  # Increase size
            resize_shape_coords(current_coords, factor)
        elif event.keysym == "Down":
            factor = 0.9  # Decrease size
            resize_shape_coords(current_coords, factor)
        elif event.keysym == "Left":
            rotate_shape(-1)  # Rotate left by 10 degrees
        elif event.keysym == "Right":
            rotate_shape(1)  # Rotate right by 10 degrees

# def resize_shape(factor):
#     if selected_shape:
#         current_coords = canvas.coords(selected_shape)
#         # Calculate center of the shape
#         x_center = (current_coords[0] + current_coords[2]) / 2
#         y_center = (current_coords[1] + current_coords[3]) / 2

#         # Resize shape around its center
#         new_coords = []
#         for i in range(len(current_coords)):
#             if i % 2 == 0:
#                 new_coords.append(x_center + (current_coords[i] - x_center) * factor)
#             else:
#                 new_coords.append(y_center + (current_coords[i] - y_center) * factor)

#         canvas.coords(selected_shape, *new_coords)



def resize_shape_coords(coords, factor):
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

    canvas.coords(selected_shape, *new_coords)

def rotate_shape(angle):
    global selected_shape
    if selected_shape:
        # Get current coordinates
        coords = canvas.coords(selected_shape)
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
        canvas.coords(selected_shape, *rotated_coords)


def change_color():
    if selected_shape:
        color = colorchooser.askcolor()
        canvas.itemconfig(selected_shape, fill=color[1])



def start_move(event):
    global selected_shape, last_x, last_y
    if event.num == 3:  # Check if right mouse button is pressed
        item = canvas.find_closest(event.x, event.y)
        if item and canvas.type(item) in ['rectangle', 'oval', 'polygon']:
            selected_shape = item
            last_x = event.x
            last_y = event.y
            canvas.bind('<B3-Motion>', move_shape)
            canvas.bind('<KeyPress-Up>', resize_up)  # Bind up arrow key for resizing up
            canvas.bind('<KeyPress-Down>', resize_down)  # Bind down arrow key for resizing down

def resize_up(event):
    global selected_shape
    if selected_shape:
        factor = 1.1  # Increase size
        resize_shape(factor)

def resize_down(event):
    global selected_shape
    if selected_shape:
        factor = 0.9  # Decrease size
        resize_shape(factor)


def move_shape(event):
    global last_x, last_y
    if selected_shape:
        dx = event.x - last_x
        dy = event.y - last_y
        canvas.move(selected_shape, dx, dy)
        last_x = event.x
        last_y = event.y


# def start_move(event):
#     global selected_shape, last_x, last_y
#     if event.num == 3:  # Check if right mouse button is pressed
#         item = canvas.find_closest(event.x, event.y)
#         if item and canvas.type(item) in ['rectangle', 'oval', 'polygon']:
#             selected_shape = item
#             last_x = event.x
#             last_y = event.y
#             canvas.bind('<B3-Motion>', move_shape)

def stop_move(event):
    if event.num == 3:  # Check if right mouse button is released
        canvas.unbind('<B3-Motion>')


        
def delete_last_shape(event):
    # Find the last drawn shape on the canvas
    last_shape = canvas.find_all()[-1] if canvas.find_all() else None
    if last_shape:
        # Delete the last drawn shape
        canvas.delete(last_shape)
        # Find and destroy the corresponding label
        label_id = f"label{last_shape}"
        label = canvas.find_withtag(label_id)
        if label:
            canvas.delete(label)
window = Tk()
window.title("Shapes")

frame = Frame(window)
frame.pack(fill=BOTH, expand=True)

menubar = Menu(window)
window.config(menu=menubar)

shapes = Menu(menubar)
menubar.add_cascade(label='Shape', menu=shapes)
shapes.add_command(label='Hexagon', command=lambda: canvas.bind('<ButtonPress-1>', lambda event: draw_shape('Hexagon', event)))
shapes.add_command(label='Circle', command=lambda: canvas.bind('<ButtonPress-1>', lambda event: draw_shape('Circle', event)))
shapes.add_command(label='Square', command=lambda: canvas.bind('<ButtonPress-1>', lambda event: draw_shape('Square', event)))
shapes.add_command(label='Triangle', command=lambda: canvas.bind('<ButtonPress-1>', lambda event: draw_shape('Triangle', event)))
shapes.add_command(label='Pentagon', command=lambda: canvas.bind('<ButtonPress-1>', lambda event: draw_shape('Pentagon', event)))
shapes.add_command(label='Change Color', command=change_color)
shapes.add_separator()
shapes.add_command(label='Exit', command=quit)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=open_project)
file_menu.add_command(label='Save As', command=save_project)

canvas = Canvas(frame, width=400, height=400, bg='#131313')
canvas.pack(fill=BOTH, expand=True)

selected_shape = None
x0, y0 = None, None
selected_shape = None
last_x, last_y = None, None



canvas.bind('<ButtonPress-3>', start_move)  
canvas.bind('<ButtonRelease-3>', stop_move)
 
window.bind('<KeyPress-Up>', resize_shape)
window.bind('<KeyPress-Down>', resize_shape)
window.bind('<KeyPress-Left>', resize_shape)
window.bind('<KeyPress-Right>', resize_shape)



# Bind the backspace key to delete the last drawn shape
window.bind('<BackSpace>', delete_last_shape)
# canvas.bind('<ButtonPress-3>', start_move)
window.mainloop()
