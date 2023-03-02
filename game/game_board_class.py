# example of drag
# https://stackoverflow.com/questions/37280004/tkinter-how-to-drag-and-drop-widgets


import tkinter as tk
from PIL import Image, ImageTk, ImageFilter, ImageDraw
from PIL import ImageEnhance as IE
from math import sqrt, pi, sin, cos
import cmath
from functools import partial
from collections import namedtuple
import fly_path as fly
import winsound as ws
import threading
import os, pickle
from run_fifo import RunFifo, fifo_run_queue

LABEL_FONT = ('Cosmic Sans MS', 12, 'normal')

fifo = RunFifo()    # queue routines that might use tkinter to animate
# @fifo_run_queue - decorator to put function call into a fifo queue; blocks queue
# fifo.complete() - unblocks fifo queue so that the next function may run
#fifo.verbose = True   # for debugging


def play_sound(name, option):
    play = lambda: ws.PlaySound(name, option)
    t = threading.Thread(target=play)
    t.start()

play_error = lambda: play_sound("error.wav", ws.SND_FILENAME)
play_alert = lambda: play_sound("SystemExclamation", ws.SND_ALIAS)

t_width, t_height = 80, 80    # tile dimesions
x_tiles, y_tiles = 8, 6         # number of tiles in game board
b_width, b_height = t_width * x_tiles, t_height * y_tiles    # game board dimensions, multiple of tile dimensions
label_height = 40
w_width, w_height = b_width, b_height + label_height    # window may be larger than game board

imgs = []    # required so that images persist
item_offset = {}    # map canvas item number to (x, y) offset relative to tile center
item_image = {}   # map canvas item number to image dict:
    # 'stack': (original, after resize, after rotate)
    # 'angle'

game = None
# Three underscores '___' in the help_msg separate tkinter Labels so as to allow hyperlinks

def get_key_text(key):
    if key == 'nine_key':
        help_keys = (
            "Nine alphabetic keys select and move a bee according to this map:\n"+
            "('qwe': 1), ('asd': 2), ('zxc': 3), ('uio': 4), ('jkl': 5), ('m,.': 6).\n"+
            "For example, 'qwe' controls bee 1. Or use the numeric keys.") 
    elif key == 'three_key':
        help_keys = (
            "Three alphabetic keys move a bee previously selected by numeric keys.\n"+
            "Use keys ('awd') for team A, or ('jil') for team B, or use the arrow keys." )
    else:
        help_keys = (
            "Six alphabetic keys control direction (NW, N, NE, SW, S, SE).\n"+
            "Use keys ('qweasd') for team A, or ('uiojkl') for team B, or use the arrows.\n" +
            "Obs., to move NW requires that arrows Left and Up are pressed at the same time.")
    return help_keys

def get_help_msg():
    help_keys = (get_key_text('nine_key') if game.option('nine_key')[0] == 'on' else
                 get_key_text('three_key') if game.option('three_key')[0] == 'on' else
                 get_key_text('six_key'))
    help_msg = (
'''Each bee is selected by number keys 1-3 (team A) or 4-6 (team B).
There are two teams, A and B. The object of the game is to kill your
opponent's bees. You move the selected bee one tile at a time by hitting a 
key.  '''+help_keys+'''

\tctrl-R\trevives killed bees
\tctrl-S\trestarts the game
\tctrl-O\toptions
\tctrl-Q\tquit
___
The red dwarf honey bee (Apis florea)
https://en.wikipedia.org/wiki/Apis_florea
___
The yellow European honey bee (Apis mellifera)
https://entnemdept.ufl.edu/creatures/MISC/BEES/euro_honey_bee.htm
'''
   )
    return help_msg

import webbrowser
def callback(url):
    webbrowser.open_new(url)
    
def frame_window(title):
    # https://stackoverflow.com/questions/28089942/
    #    difference-between-fill-and-expand-options-for-tkinter-pack-method
    window = tk.Toplevel()
    window.title(title)
    window.geometry("620x400")
    frame1 = tk.Frame(window, background='#cc5')
    frame1.pack(fill='both', expand=True)
    frame2 = tk.Frame(frame1, background='#888')
    frame2.pack(padx=8, pady=8, fill='both', expand=True)
    frame3 = tk.Frame(frame2, background='#eeb')
    frame3.pack(padx=3, pady=3, fill='both', expand=True)
    frame4 = tk.Frame(frame3, background='#eeb')
    frame4.pack(padx=10, pady=10, fill='both', expand=True)
    return window, frame4

def help():
    window, frame3 = frame_window("Honey Bee rules")
    msgs = get_help_msg().split('___')
    row = 0
    for msg in msgs:
        if 'http' in msg:
            a = [x for x in msg.split('\n') if x]
            msg, link = '\n'.join(a[:-1]), a[-1]
            height = 12
            lab = tk.Label(frame3, background='#eeb', text=msg, fg='blue', 
                           anchor=tk.NW, justify=tk.LEFT, font=("Comic Sans MS", 12))
            lab.grid(row=row, column=0, sticky=tk.W)#, padx=4, pady=4, fill='both', expand=True)
            lab.bind("<Button-1>", lambda e: callback(link)) 
        else:
            lab = tk.Label(frame3, background='#eeb', text=msg,
                           anchor=tk.NW, justify=tk.LEFT, font=("Comic Sans MS", 12))
            lab.grid(row=row, column=0)#, padx=4, pady=4, fill='both', expand=True)
        row += 1 

def options_window(options, control_keys, radio_group):
    # expect that options is a dictionary {key:(value, text)}
    window, frame = frame_window("Honey Bee options")
    def save_change():
        for i, key in enumerate(keys):
            value = var[i].get()
            other = options[key][1:]
            options.update({key: (value,) + other})
        game.game_options = save_options(options)
        window.destroy()
    keys = []
    var = []
    ctl = []
    on = []
    off = []
    row = 0
    for i, key in enumerate(options):
        if key not in control_keys:
            continue
        value, text, onvalue, offvalue = options[key]
        keys.append(key)
        var.append(tk.StringVar(value=value))
        on.append(offvalue)
        off.append(offvalue)
        ctl.append(tk.Checkbutton(frame, text=text, variable=var[-1], 
            onvalue=onvalue, offvalue=offvalue, background='#eeb', 
            anchor=tk.W, justify=tk.LEFT, font=("Comic Sans MS", 12)))
        ctl[-1].grid(row=row, column=0, sticky=tk.W)
        row += 1
    #radio = lambda i, group: [var[j].set(off[j]) for j in group if i != j]
    def radio(i, group):
        [var[j].set(off[j]) for j in group if i != j]
        text = (get_key_text('nine_key') if keys[i] == 'nine_key' and var[i].get() == 'on' else
                     get_key_text('three_key') if keys[i] == 'three_key' and var[i].get() == 'on' else
                     get_key_text('six_key'))
        lbl.config(text = '\n' + text)
    group_ids = [i for i,k in enumerate(options) if k in radio_group]
    for i in group_ids:
        ctl[i].config(command=partial(radio, i, group_ids))
    btn = tk.Button(frame, text="Save", background='#eeb', command=save_change)
    btn.grid(row=row, column=0, sticky=tk.W)
    lbl = tk.Label(frame, background='#eeb', text='...', 
        anchor=tk.W, justify=tk.LEFT, font=("Comic Sans MS", 12))
    lbl.grid(row=row+1, column=0, sticky=tk.W)
    
options_filename = 'honey_bee.pckl'
options_file_version = 1
    
def save_options(options):
    options.update({'version': options_file_version})
    with open(options_filename, 'wb') as fout:
        pickle.dump(options, fout)
    return options

def load_options(options):
    options.update({'version': options_file_version})
    if os.path.exists(options_filename):
        try:
            with open(options_filename, 'rb') as fin:
                opts = pickle.load(fin)
                if 'version' not in opts:
                    return opts   # no version control yet
                if options['version'] == opts['version']:
                    return opts
        except Exception as e:
            print('load_options: ', e)
    return options
    
def scale(r, factor):
    # scale a geometric object around its center
    x0, y0, x1, y1 = r
    cx, cy = (x0 + x1) // 2, (y0 + y1) //2
    x0 = cx + round((x0 - cx) * factor)
    x1 = cx + round((x1 - cx) * factor)
    y0 = cy + round((y0 - cy) * factor)
    y1 = cy + round((y1 - cy) * factor)
    return x0, y0, x1, y1
    
def center_item(canvas, item, bounds):
    x0, y0, x1, y1 = canvas.bbox(item)
    cx0, cy0, cx1, cy1 = bounds
    offset_x = (cx0 + cx1) // 2 - (x0 + x1) // 2 
    offset_y = (cy0 + cy1) // 2 - (y0 + y1) // 2 
    canvas.move(item, offset_x, offset_y)
    
def add_image(canvas, options):
    global imgs
    filename = options.pop('filename')
    vx0, vy0, vx1, vy1 = options.pop('viewport')
    key_id = options.pop('key_id')
    view_max = max(vx1 - vx0, vy1 - vy0)
    img0 = Image.open(filename)
    img_max = max(img0.size)
    img_size = tuple(x * view_max // img_max for x in img0.size)
    x, y = vx0, vy0
    img1 = img0.resize(img_size, Image.LANCZOS)
    img2 = ImageTk.PhotoImage(img1)
    options.update({'anchor':tk.NW, 'image':img2})
    item = canvas.create_image(x, y, options)
    dimg = {}
    dimg.update({'filename':filename, 'scale':1, 'view_max':view_max})
    dimg.update({'contrast': 1.0, 'brightness': 1.0, 'saturation': 1.0})
    dimg.update({'edge': False, 'angle': 0, 'blur': False})
    dimg.update({'angle': 0, 'key_id':key_id, 'select':0, 'stack': (img0, img1, img2)})
    item_image.update({item: dimg})
    modify_image(canvas, item, force=True)
    return item

def test_modify_image(canvas, item):
    # define kw here
    kw = {}
    test = ['scale', 'contrast', 'brightness', 'saturation', 'blur']
    i = item - 50
    kw.update({'filename': 'bee_yellow.png'})
    if i == 0:
        kw.update({'edge': True})
    if i in range(len(test)):
        kw.update({test[i]: 0.2})
    modify_image(canvas, item, **kw)
    
def modify_image(canvas, item, **kw):
    if item not in item_image:
        return
    dimg = item_image[item]
    img0, img1, img2 = dimg['stack']
    group0 = ['filename']
    group1 = ['scale', 'contrast', 'brightness', 'saturation', 'edge', 'blur', 'key_id', 'select', ]
    group2 = ['angle']
    dirty0 = dirty1 = dirty2 = False
    for key in kw:
        dirty0 = dirty0 or key in group0 and dimg[key] != kw[key]
        dirty1 = dirty1 or key in group1 and dimg[key] != kw[key]
        dirty2 = dirty2 or key in group2 and dimg[key] != kw[key]
        dimg.update({key: kw[key]})
    sw = 'force' in kw and kw['force']
    def process_scale(img, scale):
        nonlocal dimg, img0
        view_max = dimg['view_max']
        img_max = max(img0.size)
        img_size = tuple(round(x * scale * view_max // img_max) for x in img0.size)
        img1 = img0.resize(img_size, Image.LANCZOS) 
        return img1
    def process_key_id(img, key_id):
        draw = ImageDraw.Draw(img)
        w, h = img.size
        x, y, d = 24, 13, 6
        team = (key_id - 1) // 3
        for i in range((key_id - 1) % 3 + 1):
            color = '#ff5' if team==0 else '#f00' if team==1 else '#555'
            dx, dy = (0, 0) if i==0 else (-5, 7) if i==1 else (-10, 0)
            xy = (x+dx, y+dy, x+dx+d, y+dy+d)
            draw.ellipse(xy, fill=color, outline='#777')    #, outline=None, width=1)        
        return img
    def process_select_item(img, key_id):
        draw = ImageDraw.Draw(img)
        w, h = img.size
        rx, ry = 16, 9    # approximately the radius of the select graphic
        x, y = [a // 2 for a in (w, h)]
        xy = [(0, -2*ry), (-rx, 2*ry), (0, ry), (rx, 2*ry)]
        xy = [(x+dx, y+dy-3) for dx, dy in  xy]
        team = (key_id - 1) // 3
        color = '#ff5' if team==0 else '#f00' if team==1 else '#555'
        draw.polygon(xy, fill=color, outline='#555')    #, width=2)
        return img
    def process(img, key, default, func):
        nonlocal sw, kw, dimg
        if (sw or key in kw) and dimg[key] != default:
            img = func(img, dimg[key])
            sw = True
        return img
    sw = sw or dirty0
    img0 = process(img0, 'filename', '', lambda img, p: Image.open(p))
    sw = sw or dirty1
    img1 = process(img1, 'scale', None, process_scale)  # None means to do this if sw is dirty
    img1 = process(img1, 'contrast', 1.0, lambda img, p: IE.Contrast(img).enhance(p))
    img1 = process(img1, 'brightness', 1.0, lambda img, p: IE.Brightness(img).enhance(p))
    img1 = process(img1, 'saturation', 1.0, lambda img, p: IE.Color(img).enhance(p))
    img1 = process(img1, 'edge', False, lambda img, p: img.filter(ImageFilter.EDGE_ENHANCE))
    img1 = process(img1, 'blur', False, lambda img, p: img.filter(ImageFilter.BLUR))
    img1 = process(img1, 'key_id', 0, process_key_id)
    img1 = process(img1, 'select', 0, process_select_item)
    sw = sw or dirty2
    key = 'angle'
    if sw or 'angle' in kw:
        dimg.update({'stack': (img0, img1, img2)})
        item_image.update({item: dimg})
        rotate_item(canvas, item, dimg['angle'])

def rotate_item(canvas, item, angle):
    # https://stackoverflow.com/questions/15736530/python-tkinter-rotate-image-animation
    # https://pillow.readthedocs.io/en/stable/reference/Image.html#the-image-class
    # img is of pillow class Image
    if item not in item_image:
        return
    dimg = item_image[item]
    img0, img1, img2 = dimg['stack']
    tmp = img1.rotate(angle)
    img2 = ImageTk.PhotoImage(tmp)
    dimg.update({'stack': (img0, img1, img2), 'angle': angle})
    item_image.update({item: dimg})
    item = canvas.itemconfig(item, image=img2)  
    canvas.angle = angle % 360

def rotate_item_smoothly(canvas, item, angle):
    canvas._drag_item = item
    cx1, cy1 = get_tile_center(canvas, item)
    offx, offy = item_offset[item]
    animate_snap(canvas, cx1+offx, cy1+offy, angle)
    
def mirror_image(canvas, item):
    #image = ImageOps.mirror(image)
    pass

def delete_item_piece(canvas, item):
    if item in canvas.item_piece:
        item_piece.pop(item)
        
def add_item_piece(canvas, item, piece):
    item = item if type(item) in (tuple, list) else [item]
    for it in item:
        canvas.item_piece.update({it: piece})

def delete_family(canvas, item):
    if item in canvas.fam_parents:
        parent = canvas.fam_parents[item]
        canvas.fam_parents.pop(item)
        canvas.fam_children[parent].pop()
        s = canvas.fam_children[parent]
        if not s:
            canvas.fam_children.pop(parent)
    
def add_family(canvas, parent, child):
    child = child if type(child) in (tuple, list) else [child]
    for ch in child: 
        canvas.fam_parents.update({ch: parent})
        s = canvas.fam_children[parent] if parent in canvas.fam_children else set()
        s.add(ch)
        canvas.fam_children.update({parent: s})

def is_draggable(canvas, item):
    item = item[0] if type(item) == tuple else item
    return item in canvas.draggable_items

def get_item_center(canvas, item):
    px0, py0, px1, py1 = canvas.bbox(item)
    cx0, cy0 = (px0 + px1) // 2, (py0 + py1) // 2
    return cx0, cy0
    
def get_tile_center(canvas, item):
    # return tile center
    cx0, cy0 = get_item_center(canvas, item)
    w, h = t_width, t_height
    half_height = h // 2
    cx1, cy1 = cx0 // w * w + w // 2, cy0 // h * h + h // 2
    
    # adjust for hexagon offset
    if canvas.pattern == pattern_hexagon:
        cy1 = (cy0 - half_height) // h * h + h if (cx1 // w) % 2 == 1 else cy1
    
    # keep inbounds
    cx1 = w//2 if cx1 < 0 else b_width-w//2 if cx1 > b_width else cx1
    cy1 = h//2 if cy1 < 0 else b_height-h//2 if cy1 > b_height else cy1        
    return cx1, cy1

def make_board_clickable(canvas, item):
    canvas.tag_bind(item, "<Button-1>", on_board_click)
    
def make_draggable(canvas, item, child=None):
    item = item[0] if type(item) == tuple else item
    parent, item = (item, child) if child else (None, item)
    canvas.draggable_items.append(item)
    canvas.tag_bind(item, "<Button-1>", on_drag_start)
    canvas.tag_bind(item, "<B1-Motion>", on_drag_motion)
    canvas.tag_bind(item, "<ButtonRelease-1>", on_drag_stop)
    r = canvas.coords(item)
    cx0, cy0 = get_item_center(canvas, item)
    cx1, cy1 = get_tile_center(canvas, item)
    item_offset.update({item: (cx0 - cx1, cy0 - cy1)})

def deselect_item(canvas, call_modify_image=True):
    if canvas.active_item:
        item = canvas.active_item
        parent = canvas.fam_parents[item] if item in canvas.fam_parents else item
        piece = canvas.item_piece[parent]
        canvas.delete(item)
        canvas.delete_family(item)
        modify_image(canvas, parent, select=0, edge=False)
        canvas.active_item = None
        
def select_item(canvas, item):
    piece = canvas.item_piece[item]
    if canvas.active_item in piece.items:
        return
    deselect_item(canvas, False)
    x0, y0, x1, y1 = scale(piece.bbox(), 0.65)
    r = (x1 - 1, y0, x1, y0 + 1)
    modify_image(canvas, item, select=piece.key_id, edge=True)
    canvas.active_item = canvas.create_oval(*r, fill='#4f4')
    canvas._drag_item = piece.item
    canvas.angle = (piece.last_direction - 90) % 360
    piece.items.append(canvas.active_item)
    canvas.add_family(piece.item, canvas.active_item)
    lift_item(canvas, item)
        
def is_selected(canvas, item):
    # active_item points to graphic showing activation
    parent = canvas.fam_parents[item] if item in canvas.fam_parents else item
    if parent not in canvas.item_piece: return False
    return canvas.active_item in piece.items

def lift_item(canvas, item):
    item = item[0] if type(item) == tuple else item
    if item in canvas.fam_parents or item in canvas.fam_children:
        parent = canvas.fam_parents[item] if item in canvas.fam_parents else item
        siblings = canvas.fam_children[parent]
        canvas.lift(parent) 
        for child in siblings: 
            canvas.lift(child) 
    else:
        canvas.lift(item)         

def move_item(canvas, item, dx, dy):
    item = item[0] if type(item) == tuple else item
    if item in canvas.fam_parents or item in canvas.fam_children:
        parent = canvas.fam_parents[item] if item in canvas.fam_parents else item
        siblings = canvas.fam_children[parent]
        canvas.move(parent, dx, dy) 
        for child in siblings: 
            canvas.move(child, dx, dy) 
    else:
        canvas.move(item, dx, dy)         
    
def on_drag_start(event):
    canvas = event.widget
    canvas._drag_item = None
    canvas._drag_motion = False
    item = canvas.find_closest(event.x, event.y)
    item = item[0] if type(item) == tuple else item
    if not is_draggable(canvas, item): return
    deselect_item(canvas)
    canvas._drag_item = item
    canvas._drag_first_x = event.x
    canvas._drag_first_y = event.y
    canvas._drag_last_x = event.x
    canvas._drag_last_y = event.y
    canvas._drag_item_offset = item_offset[item]
    canvas.angle = 0
    lift_item(canvas, item)

import cmath
def to_polar(dx, dy):
    r, a = cmath.polar(complex(dx, dy))
    return r, a % (2 * pi)

def on_drag_motion(event):
    canvas = event.widget
    item = canvas._drag_item
    if item == None: return
    if abs(event.x - canvas._drag_first_x) + abs(event.y - canvas._drag_first_y) < 5: return
    canvas._drag_motion = True
    dx = event.x - canvas._drag_last_x
    dy = event.y - canvas._drag_last_y
    canvas._drag_last_x = event.x
    canvas._drag_last_y = event.y
    move_item(canvas, item, dx, dy)
    if 'angle' in canvas.options and 'drag_motion' in canvas.options['angle']:
        r, angle = to_polar(event.x - canvas._drag_first_x, -(event.y - canvas._drag_first_y))
        canvas.angle = int(angle * 180 / pi - 90) % 360
        rotate_item(canvas, item, canvas.angle)

def animate_snap(canvas, cx1, cy1, angle1, i=20, fl=None):
    # angle is in degrees
    item = canvas._drag_item
    cx0, cy0 = get_item_center(canvas, item)
    angle0 = canvas.angle
    if angle1 - angle0 > 185:
        angle1 -= 360
    elif angle1 - angle0 < -185:
        angle1 += 360
    if fl == None:
        fl = fly.Fly((cx0, cy0, angle0), (cx1, cy1, angle1), next_point = fly.next_point_straight)
        fl = iter(fl)
    complete = False
    try:
        x, y, angle = next(fl)
        dx, dy = x - cx0, y - cy0
    except StopIteration:
        angle = angle1
        angle = round(angle / 60) * 60
        dx, dy = cx1 - cx0, cy1 - cy0
        complete = True
    else:
        fifo.keep_blocking(20)
        canvas.after(10, animate_snap, canvas, cx1, cy1, angle1, i-1, fl)
    move_item(canvas, item, dx, dy)
    if 'angle' in canvas.options and 'drag_stop' in canvas.options['angle']:
        rotate_item(canvas, item, angle)
    if complete:
        game.kill_bees(item, cx1, cy1)
        bee = game.get_bee_from_item(item)
        bee.last_direction = angle + 90
        game.toggle_team()
        fifo.complete()
    
def animate_snap_old(canvas, cx1, cy1, angle1, i=20):
    item = canvas._drag_item
    cx0, cy0 = get_item_center(canvas, item)
    angle0 = canvas.angle
    dangle = (angle1 - angle0) * (20 - i) // 20
    angle = angle0 + dangle
    dx, dy = cx1 - cx0, cy1 - cy0
    if i > 1 and abs(dx) + abs(dx) + abs(dangle) > 0:
        sign = lambda x: -1 if x<0 else 1
        dx = round(sign(dx) * sqrt(abs(dx)) * 0.7)
        dy = round(sign(dy) * sqrt(abs(dy)) * 0.7)
        canvas.after(10, animate_snap_old, canvas, cx1, cy1, angle1, i-1)
    move_item(canvas, item, dx, dy)
    if 'angle' in canvas.options and 'drag_stop' in canvas.options['angle']:
        rotate_item(canvas, item, angle)
    
def on_drag_stop(event):
    canvas = event.widget
    item = canvas._drag_item
    if item == None:
        return
    if not canvas._drag_motion:
        select_item(canvas, item)
        #call_back needed - see select_bee
        return
    cx1, cy1 = get_tile_center(canvas, item)
    offx, offy = canvas._drag_item_offset
    angle = canvas.angle
    animate_snap(canvas, cx1+offx, cy1+offy, angle)

def on_board_click(event):
    canvas = event.widget
    item = canvas.active_item
    if not item: return
    item = canvas.fam_parents[item] if item in canvas.fam_parents else item
    board_item = canvas.find_closest(event.x, event.y)
    cx1, cy1 = get_tile_center(canvas, board_item)
    cx0, cy0 = get_tile_center(canvas, item)
    offx, offy = item_offset[item]
    if 'angle' in canvas.options and 'drag_motion' in canvas.options['angle']:
        if (cx1 == cx0) and (cy1 == cy0):  # can happen if item is on edge of board
            r, angle = to_polar(event.x - cx0, -(event.y - cy0))
        else:
            r, angle = to_polar(cx1 - cx0, -(cy1 - cy0))
        angle = int(angle * 180 / pi - 90) % 360
        #rotate_item(canvas, item, angle)    
    animate_snap(canvas, cx1+offx, cy1+offy, angle)

def pattern_random(i, j):
    from random import randint
    ranx = lambda: f"{randint(0, 255):x}".zfill(2)
    options = {'fill': f"#{ranx()}{ranx()}{ranx()}"}
    return options

def pattern_checkered(i, j):
    odd = (i + j) % 2
    options = {'fill': "#866" if not odd else "#ddd"}
    return options

def pattern_granite(i, j):
    global imgs
    odd = (i + j) % 2
    filename = "light_granite_100.png" if not odd else "dark_granite_100.png"
    img = tk.PhotoImage(file=filename)
    imgs.append(img)
    options = {'image': img, 'anchor': tk.NW}
    return options

def pattern_hexagon(i, j, scheme = 'default'):
    # table of offsets in x and y
    long_axis = t_width * 4 // 3
    x0, x1, x2, x3 = 0, long_axis // 4, long_axis * 3 // 4, long_axis
    y0, y1, y2 = 0, t_height // 2, t_height
    
    # get color of tile
    if scheme == 'random':
        options = pattern_random(i, j)
    elif scheme == 'rgb':
        color_index = (i % 2 + 2 - j % 3) % 3    # magic needed to alternate colors
        colors = {0: '#c33', 1: '#3c3', 2: '#33c'}
        options = {'fill': colors[color_index]}
    else:
        options = {'fill': '#ee8', 'outline': '#cc6', 'width': 1}  # more like hive color?
        # options = {'fill': '#cc5', 'outline': '#888', 'width': 2}  # original
        
    # get shape of hexagon, then offset x, y
    odd = (i + j) % 2
    pgon = (0, y1, x1, 0, x2, 0, x3, y1, x2, y2, x1, y2)
    pgon = (a if not odd else a for a in pgon)
    options.update({'polygon': pgon})
    return options

class Canvas(tk.Canvas):
    options = {}
    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)
        self.draggable_items = []
        self.fam_parents = {}   # map child to parent id
        self.fam_children = {}    # map parent to set of children ids
        self.item_piece = {}
        self.place(x=0, y=0)

    def __getattr__(self, attr):
        # return dispatcher which calls function of form "attr(canvas, ...)"
        #return CanvasDispatcher(self, attr)
        return partial(globals()[attr], self)
    
# attach functions as methods, as alternative to Dispatcher example above
#setattr(Canvas, 'rotate_item', rotate_item)

class Board(Canvas):
    def __init__(self, *p, **kw):
        self.frame = p[0]
        global t_width, t_height, b_width, b_height, w_width, w_height
        self.pattern = kw.pop('pattern') if 'pattern' in kw else pattern_checkered
        if self.pattern == pattern_hexagon:
            long_axis = t_width * 4 // 3
            t_height = long_axis * 86 // 100
            b_width = t_width * x_tiles + t_width // 3
            b_height = t_height * y_tiles + t_height // 2
            kw.update({'width': b_width, 'height': b_height})
        super().__init__(*p, **kw)
        self.rows = []
        for j in range(y_tiles): 
            row = []
            for i in range(x_tiles):
                x, y = t_width * i, t_height * j
                if self.pattern == pattern_granite:
                    item = self.create_image(x, y, **self.pattern(i, j))
                elif self.pattern == pattern_hexagon:
                    x, y = t_width * i, t_height * j
                    pat = self.pattern(i, j)
                    y_offset = t_height // 2 if i % 2 == 1 else 0
                    poly0 = tuple(pat.pop('polygon'))
                    poly1 = tuple(v + x if iv % 2 == 0 else v + y + y_offset for iv, v in enumerate(poly0))
                    item = self.create_polygon(*poly1, **pat)
                else:
                    rec = (x, y, x + t_width, y + t_height)
                    item = self.create_rectangle(*rec, **self.pattern(i, j))
                make_board_clickable(self, item)
                row.append(item)
            self.rows.append(row)
    
class Piece:
    last_piece_key_id = 0
    def __init__(self, board, i, j, **options): 
        # i, j is the x, y position on the board
        Piece.last_piece_key_id += 1
        self.key_id = Piece.last_piece_key_id
        self.board = board
        canvas = self.board
        board_item = self.board.rows[j][i]
        canvas.active_item = None     # points to the selection indicating item, not the parent
        x0, y0, x1, y1 = bbox = canvas.bbox(board_item)
        self.team = options.pop('team') if 'team' in options else ''
        self.dead = False
        if "filename" in options: 
            bbox2 = scale(bbox, 0.8)
            options.update({'viewport':scale(bbox, 0.8)})
            options.update({'key_id':self.key_id})
            self.item = add_image(canvas, options)
            self.items = [self.item]
            canvas.center_item(self.items[0], canvas.bbox(board_item))
            canvas.make_draggable(self.items[0])
        else:
            r = scale(bbox, 0.7)
            r1 = scale(r, 0.7)
            r2 = list(r); r2[2] = r2[0] + 5
            color = options["color"] if "color" in options else "#e50"
            self.item = canvas.create_oval(*r, outline="#aaa", fill=color)   # parent
            self.items = [self.item]
            self.items.append(canvas.create_rectangle(*r1, outline="#aaa", fill="#5c5"))
            #self.items.append(canvas.create_rectangle(*r2, outline="#aaa", fill="#55c"))
            for i in self.items: make_draggable(canvas, i)
        add_family(canvas, self.items[0], self.items[1:])
        add_item_piece(canvas, self.items, self)
        self.last_direction = 90
        
    def __getattr__(self, attr):
        #return PieceDispatcher(self, attr)
        yes = attr in dir(self.board)
        from pprint import pprint
        #foo = eval('Canvas.' + attr if yes else attr)
        foo = getattr(Canvas, attr) if yes else globals()[attr]
        if 'create' == attr[:6]:
            return partial(foo, self.board)
        else:
            return partial(foo, self.board, self.item)

class Game:
    def __init__(self):
        global w_width, w_height
        self.window = tk.Tk()

        def add_label(text, sticky):
            label = tk.Label(self.window, text=text, font=LABEL_FONT, bg='#555', fg='#ffb') 
            label.grid(row=0, column=0, sticky=sticky)
            return label
        self.label1 = add_label(' team A ', tk.W)
        self.label = add_label('Type "H" for help', tk.N)
        self.label3 = add_label(' team B ', tk.E)

        #self.frame = tk.Frame(self.window, width=b_width, height=b_height)
        #self.frame.grid(row=1, column=0)
        self.frame = self.window
        #pattern = pattern_random
        #pattern = pattern_checkered
        #pattern = pattern_granite
        pattern = pattern_hexagon
        pattern(0, 0)    # allow pattern to initialize b_width, b_height
        self.board = Board(self.window, pattern=pattern, 
                           width=b_width, height=b_height, bg='#985')  # was bg='#555'
        self.board.grid(row=1, sticky=tk.W)
        #self.frame.config(width=b_width, height=b_height)
        w_width, w_height = b_width, b_height + label_height
        self.window.geometry(f"{w_width}x{w_height}")
        canvas = self.board
        canvas.options = {'angle': 'drag_motion, drag_stop'}
        def add_piece(i, j, filename, team, angle):
            p = Piece(self.board, i, j, filename=filename, team=team)
            self.rotate_bee(p, angle)
            p.start = (i, j, angle)
            return p
        self.pieces = []
        for j in range(2, 5):
            self.pieces.append(add_piece(0, j, "bee_yellow.png", "A", 30))
        for j in range(2, 5):
            self.pieces.append(add_piece(x_tiles-1, j-1, "bee_red.png", "B", 180+30))
        self.key_id_to_piece = {p.key_id: p for p in self.pieces}
        self.direction = {'NW': 90+60, 'N': 90, 'NE': 90-60, 
                          'SW': 270-60, 'S': 270, 'SE': 270+60}
        self.direction_msg = {self.direction[k]: k for k in self.direction}
        self.game_options = {
            'three_key': ('on', 'Three keys - use to move (left, right, straight)',
                'on', 'off'),
            'nine_key': ('off', 'Nine keys - row selects bee and column gives direction',
                'on', 'off'),
            'toggle_team': ('off', 'Team switches after a move',
                'on', 'off')
        }
        self.game_options = load_options(self.game_options)
        self.radio_group = ('three_key', 'nine_key')  # "six_key" is implied when others are off
        self.control_keys = self.radio_group + ('toggle_team',)
        self.history = []   # manditory key: team
        self.team = None
        self.team_bee_id = {'A': None, 'B': None}   # bee_id (int 1-6) selected for that team
    
    def option(self, key, value=None):
        if value:
            text = self.game_options[key][1]
            self.game_options.update({key:(value, text)})
        else:
            return self.game_options[key]
    
    def set_state(self, **state):
        self.team = state['team']
        bee_id = state['bee_id'] if 'bee_id' in state else None
        if self.team:
            self.team_bee_id.update({self.team:bee_id})
        self.history.append(state)
        if len(self.history) > 10:
            self.history.pop(0)
    
    def do_undo(self):
        if self.history:
            state = self.history.pop()
            self.team = state['team']
            bee_id = state['bee_id'] if 'bee_id' in state else None
            if self.team:
                self.team_bee_id.update({self.team:bee_id})
            # add action to restore last position and rotation of bee
    
    def toggle_team(self):
        if self.option('toggle_team')[0] == 'on':          
            self.team = 'A' if self.team == 'B' else 'B'
            bee_id = self.team_bee_id[self.team]
            if bee_id:
                self.select_bee(str(bee_id))
            else:
                self.highlight_team_label(self.team)
            
    def bee_selected(self):
        board = self.board
        item = board.active_item
        if not item: return None
        item = board.fam_parents[item] if item in board.fam_parents else item
        if item not in board.item_piece: return False
        bee = board.item_piece[item]
        return bee
    
    def get_bee_from_ch(self, ch):
        key_id = int(ch) if ch.isdigit() else None
        if key_id not in self.key_id_to_piece: return None
        bee = self.key_id_to_piece[key_id]
        return bee
    
    def get_bee_from_item(self, item):
        for p in self.pieces:
            if p.item == item:
                return p
        return None
        
    def highlight_team_label(self, bee=None):
        bold_font = LABEL_FONT[:1] + (14, 'bold',)
        self.label1.config(font=LABEL_FONT, bg='#555', fg='#ee8')
        self.label3.config(font=LABEL_FONT, bg='#555', fg='#ee8')
        if type(bee) == Piece and bee.team[-1] == 'A':
            self.label1.config(font=bold_font, bg='#999', fg='#ffa')
        elif type(bee) == Piece and bee.team[-1] == 'B':
            self.label3.config(font=bold_font, bg='#999', fg='#ffa')
        elif self.team == 'A':
            self.label1.config(font=bold_font, bg='#999', fg='#ffa')
        elif self.team == 'B':
            self.label3.config(font=bold_font, bg='#999', fg='#ffa')
    
    def deselect_bee(self):
        deselect_item(self.board)
        self.highlight_team_label()

    def select_bee(self, ch):
        bee = self.get_bee_from_ch(ch)
        if not bee: 
            play_error()
            return None
        elif bee.dead:
            self.label.config(text='Cannot select a dead bee')
            #play_error()
            if True and bee == self.bee_selected():
                self.deselect_bee()
            return None
        select_item(self.board, bee.item)
        self.board.angle = (bee.last_direction - 90) % 360
        self.highlight_team_label(bee)
        return bee

    def rotate_bee(self, bee, direction):
        # angle from x-axis, counter-clockwise
        assert (direction - 30) % 60 == 0, 'rotate_bee angle must be multiple of 60 starting with 30'
        bee.last_direction = direction
        rotate_item(self.board, bee.item, direction-90)
    
    def rotate_bee_smoothly(self, bee, direction):
        # angle from x-axis, counter-clockwise
        assert (direction - 30) % 60 == 0, 'rotate_bee angle must be multiple of 60 starting with 30'
        bee.last_direction = direction
        rotate_item_smoothly(self.board, bee.item, direction-90)
    
    def move_bee(self, direction):
        # move one tile; angle from x-axis, counter-clockwise
        assert (direction - 30) % 60 == 0, 'rotate_bee angle must be multiple of 60 starting with 30'
        def delta_angle(diff):
            c = abs(diff) % 360
            return c if c < 180 else 360 - c
        bee = self.bee_selected()
        if not bee: return
        if self.option('three_key')[0] == 'on' or self.option('nine_key')[0] == 'on':
            direction = (bee.last_direction + direction - 90) % 360
        if delta_angle(bee.last_direction - direction) > 60:
            self.label.config(text = 'Bee direction restricted to +/- 60 degrees-')
            return
        bee.last_direction = direction
        self.label.config(text = self.direction_msg[direction])
        cx, cy = get_item_center(self.board, bee.item)
        angle = direction * pi / 180
        dx, dy = t_width * cos(angle), -t_height * sin(angle)
        x, y = cx + dx, cy + dy
        tiles = self.board.find_overlapping(x, y, x+1, y+1)
        if len(tiles) >= 1:
            event = namedtuple('Event', 'widget, x, y')(self.board, x, y)
            on_board_click(event)
        else:
            self.rotate_bee_smoothly(bee, direction)
    
    def kill_bees(self, attacker, xa, ya):
        # check if covering a bee and kill it.
        if type(attacker) == int:
            attacker = self.get_bee_from_item(attacker)
        board_item = self.board.find_closest(xa, ya)
        x, y = get_tile_center(self.board, board_item)
        dead_bees = [b for b in self.pieces
                     if not b.dead
                     and (x, y) == get_tile_center(self.board, b.item)
                     and b.team != attacker.team]
        for db in dead_bees:
            if db == self.bee_selected():
                self.deselect_bee()            
            db.dead = True
            self.team_bee_id.update({db.team:None}) 
            self.board.itemconfigure(db.item, state='hidden')
        return
    
    def revive_bees(self, bee):
        self.label.config(text = 'revive')
        if type(bee) in (list, tuple):
            for b in bee:
                self.revive_bees(b)
            return
        bee.dead = False
        self.board.itemconfigure(bee.item, state='normal')
    
    def restart_game(self):
        deselect_item(self.board)
        self.revive_bees(self.pieces)
        for p in self.pieces:
            i, j, angle = p.start
            board_item = i + j * x_tiles + 1
            cx1, cy1 = get_tile_center(self.board, board_item)
            cx0, cy0 = get_tile_center(self.board, p.item)
            move_item(self.board, p.item, cx1-cx0, cy1-cy0)
            self.rotate_bee(p, angle)
        self.label.config(text = 'restart game')
        self.highlight_team_label()

    def do_escape(self, ch):
        pass
    
    @fifo_run_queue
    def do_something(self, ch):
        # respond to keyboard character
        if self.option('nine_key')[0] == 'on':
            mapp = [(1,'qwe'), (2,'asd'), (3,'zxc'), (4,'uio'), (5,'jkl'), (6,'m,.'), ]
            bee_id = tuple(i for i, s in mapp if ch in s)
            direction = {'q': 90+60, 'w': 90, 'e': 90-60, 'u': 90+60, 'i': 90, 'o': 90-60, 
                         'a': 90+60, 's': 90, 'd': 90-60, 'j': 90+60, 'k': 90, 'l': 90-60, 
                         'z': 90+60, 'x': 90, 'c': 90-60, 'm': 90+60, ',': 90, '.': 90-60}
        elif self.option('three_key')[0] == 'on':
            direction = {'a': 90+60, 'w': 90, 'd': 90-60, 'j': 90+60, 'i': 90, 'l': 90-60}
        else:
            direction = {'q': 90+60, 'w': 90, 'e': 90-60, 'a': 270-60, 's': 270, 'd': 270+60,
                         'u': 90+60, 'i': 90, 'o': 90-60, 'j': 270-60, 'k': 270, 'l': 270+60}        
        if ch.isdigit():
            ch = str(int(ch) - 3) if ch in '789' else ch
            team = 'A' if ch in '123' else 'B' if ch in '456' else None
            if team:
                self.team = team
                bee = self.select_bee(ch)
                if bee:
                    self.team_bee_id.update({self.team:int(ch)})            
        elif ch in direction:
            if self.option('nine_key')[0] == 'on' and bee_id:
                bee_id = bee_id[0]
                team = 'A' if ch in 'qweasdzxc' else 'B' if ch in 'uiojklm,.' else None
                if self.option('toggle_team')[0] == 'on':
                    if team and self.team and team != self.team:
                        self.label.config(text = 
                            f'Select bee from team {self.team} in order to move it.')
                        return
                bee = self.select_bee(str(bee_id))
                if bee:
                    self.team = team
                    self.team_bee_id.update({self.team:bee_id})  
                    self.move_bee(direction[ch])
            elif not self.bee_selected():
                self.label.config(text = 'Select bee in order to move it.')
            else:
                self.move_bee(direction[ch])
        elif ch in ('h', 'H'):
            help()
    
    @fifo_run_queue
    def do_arrow_key(self, sym):
        def after_delay(sym):
            if self.option('three_key')[0] == 'on':
                key_map = {'Left': 'NW', 'Up': 'N', 'Right': 'NE'}
                if sym in key_map:
                    key = key_map[sym]
                    self.move_bee(self.direction[key])
            elif self.arrow_key_state not in (None, 'first_found'):
                syms = (self.arrow_key_state, sym)
                key = ('NW' if 'Up' in syms and 'Left' in syms else
                       'SW' if 'Down' in syms and 'Left' in syms else
                       'NE' if 'Up' in syms and 'Right' in syms else
                       'SE' if 'Down' in syms and 'Right' in syms else None)
                if key in self.direction:
                    self.move_bee(self.direction[key])
            elif sym == 'Up':
                key = 'N'
                self.move_bee(self.direction[key])
            elif sym == 'Down':
                key = 'S'
                self.move_bee(self.direction[key])
            else:
                key = sym
            self.arrow_key_state = None
        if self.option('nine_key')[0] == 'on':
            pass
        elif self.option('three_key')[0] == 'on':
            after_delay(sym)
        elif not self.arrow_key_state:
            self.arrow_key_state = 'first_found'
            self.board.after(200, after_delay, sym)
        elif self.arrow_key_state == 'first_found':
            self.arrow_key_state = sym
        else:
            self.arrow_key_state = None
                     
    def mainloop(self): 
        self.window.mainloop()

if __name__ == "__main__":
    game = Game()
    game.arrow_key_state = None    # handle double arrow key (None, 'first_found', event.keysym)
    def key(event):
        fifo.complete_if_timed_out()
        key_type = ('normal' if event.char == event.keysym else
                    'punctuation' if len(event.char) == 1 else
                    'special_key'    # in event.keysym
                    )
        if key_type == 'normal':
            game.do_something(event.char)
        elif key_type == 'punctuation':
            if event.char in ',.':
                game.do_something(event.char)
            elif event.keysym == 'r':
                game.revive_bees(game.pieces)
            elif event.keysym == 's':   # char='\x13', control char
                game.restart_game()
            elif event.keysym == 'o':
                options_window(game.game_options, game.control_keys, game.radio_group)
            elif event.keysym == 'h':
                help()
            elif event.keysym == 'q':
                game.window.quit()
            elif event.keysym == 'Escape':
                game.do_escape()
        elif key_type == 'special_key':
            if event.keysym in ('Left', 'Right', 'Up', 'Down'):
                game.do_arrow_key(event.keysym)
    game.window.bind_all('<Key>', key)
    
    # set window position and other attributes
    ws = game.window.winfo_screenwidth() # width of the screen
    hs = game.window.winfo_screenheight() # height of the screen
    w, h = w_width+5, w_height
    x, y = ws - w - 10, 50
    #w, h, x, y = ws, hs, 0, 0
    game.window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    game.window['bg'] = '#555'  # could use window.configure(bg='')
    #game.window.overrideredirect(1)
    #game.window.wm_attributes('-transparentcolor','#555')   #555 is the board background
    
    game.mainloop()
    save_options(game.game_options)

