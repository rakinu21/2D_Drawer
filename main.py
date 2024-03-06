
from tkinter import *
from tkinter import colorchooser
from golbal import Global 
from shapes.hexagon import HexagonDrawer 
from shapes.pentagon import PentagonDrawer
from shapes.circle import CircleDrawer
from shapes.square import SquareDrawer
from shapes.triangle import TriangleDrawer
from edit.delete import ShapeDeleter
from save.openfile import ProjectOpener
from save.saveFile import ProjectSaver

def pick_color():
    if Global.shape is None:
        return 
    Global.shape.change_color()

def size_shape(event):
    if Global.resize is None:
        return
    Global.resize.resize_shape(event)

def Move_Zome(event):
    if Global.move_and_zome is None:
        return
    Global.move_and_zome.start_move(event)   

def save_proj():
    Save_project.save_project()

def open_project():
    openFile.open_project()

window = Tk()
window.title("Shapes")

frame = Frame(window)
frame.pack(fill=BOTH, expand=True)

menubar = Menu(window,background='#000000')
window.config(menu=menubar ,bg='#000000')

shapes_menu = Menu(menubar,bg='#ffffff',font=('Copperplate Gothic Bold',10),fg='#000000',tearoff=0 )
menubar.add_cascade(label='Shape', menu=shapes_menu, font=('Copperplate Gothic Bold',10))
shapes_menu.add_command(label='Hexagon', command=lambda: canvas.bind('<ButtonPress-1>', lambda event: hexagon_drawer.draw_shape(event)))
shapes_menu.add_command(label='Circle', command=lambda: canvas.bind('<ButtonPress-1>', lambda event: circle_drawer.draw_shape(event)))
shapes_menu.add_command(label='Square', command=lambda: canvas.bind('<ButtonPress-1>', lambda event: square_drawer.draw_shape(event)))
shapes_menu.add_command(label='Triangle', command=lambda: canvas.bind('<ButtonPress-1>', lambda event: triangle_drawer.draw_shape(event)))
shapes_menu.add_command(label='Pentagon', command=lambda: canvas.bind('<ButtonPress-1>', lambda event: pentagon_drawer.draw_shape(event)))
shapes_menu.add_command(label='Change Color', command= pick_color)
shapes_menu.add_separator()
shapes_menu.add_command(label='Exit', command=quit)

file_menu = Menu(menubar, tearoff=0,bg='#ffffff',font=('Copperplate Gothic Bold',10),fg='#000000')
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=  open_project)
file_menu.add_command(label='Save As', command= save_proj)

canvas = Canvas(frame, width=600, height=400, bg='#131313')
canvas.pack(fill=BOTH, expand=True)

selected_shape = None
hexagon_drawer = HexagonDrawer(canvas)
circle_drawer = CircleDrawer(canvas)
square_drawer = SquareDrawer(canvas)
triangle_drawer = TriangleDrawer(canvas)
pentagon_drawer = PentagonDrawer(canvas)
shape_deleter = ShapeDeleter(canvas)

Save_project =  ProjectSaver(canvas)
openFile = ProjectOpener(canvas)



# Bind the BackSpace key to the delete_last_shape method of ShapeDeleter
window.bind('<BackSpace>', shape_deleter.delete_last_shape)
window.bind('<KeyPress-Up>',size_shape)
window.bind('<KeyPress-Down>',size_shape)
window.bind('<KeyPress-Left>',size_shape)
window.bind('<KeyPress-Right>',size_shape)
window.bind('<ButtonPress-3>', Move_Zome)  
window.mainloop()


