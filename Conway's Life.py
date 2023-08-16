#!/usr/bin/env python3
#
# Conway's game of life
# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
# James Nash
# built on framework from Henrik Tunedal
# Copyright 2023 James Nash, Henrik Tunedal. Licensed under the MIT license.
#
# Points of interest (from HT's framework):
#
#   * The model classes have no knowledge of Tkinter. This makes them
#     possible to test and debug without starting up the GUI.
#
#   * There are no global variables. Objects are created in the main
#     function and passed as parameters.
#
#   * The BoardState class is split out from GameBoardModel to
#     simplify resetting the game.
#
help_string = '''Using this demo
Click on Enter to select or deselect cells.
Click on Run to run the game of life.
Click on Run again to stop the game.
Click on Reset to reload the last pattern entered
'''

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
from functools import partial
import copy, json, os
from list_window import ListWindow

time_test = False
import time
t0 = None

def main():
    root = tk.Tk()
    board = GameBoardModel()

    build_ui(root, board)

    root.title("Life")
    root.geometry("500x550")
    root.mainloop()

def elapse_time(text):
    global t0
    if time_test:
        t = round(time.time() * 1000)   
        if t0:
            print(text, t-t0)
        t0 = t

def build_ui(root, board):
    def on_button_click(col, row, text):
        board.button_click(text)
    
    def on_canvas_click(event):
        col, row = round(event.x//board.x_size), round(event.y//board.y_size)
        board.place_mark(col, row)

    def on_move(player, col, row):
        buttons[row * 3 + col].configure(text=player)

    def on_game_state_change(mode):
        pass

    def create_button(col, row, text):
        b = ttk.Button(root, command=partial(on_button_click, col, row, text), text=text)
        b.grid(column=col, row=row, sticky="nw")
        return b
    
    def create_canvas(span):
        global line
        c = tk.Canvas(root, bg="white", height=500, width=500)
        c.grid(column=0, row=1, sticky='nw', columnspan=span)
        c.bind('<Button-1>', on_canvas_click)
        draw_grid(c)
        return c
        
    def draw_grid(c):
        global line
        for i in range(board.x_tiles):
            line=c.create_line(0, i*board.y_size, 500, i*board.y_size, fill='#aaa')
            line=c.create_line(i*board.x_size, 0, i*board.x_size, 500, fill='#aaa')
    
    def draw_board(cells):
        elapse_time('draw_board')
        canvas.delete("all")
        draw_grid(canvas)
        for i in range(board.x_tiles):
            for j in range(board.y_tiles):
                coord = (i * board.x_size + 1, j * board.y_size + 1, 
                         i * board.x_size + board.x_size - 2, j * board.y_size + board.y_size - 2)
                fill = '#f00' if cells[i*board.x_tiles + j] == 1 else '#fff'
                canvas.create_rectangle(coord, fill=fill, outline=fill)
    
    def periodic_service():
        if board.mode =='run':
            elapse_time('periodic_service')
            board.update_cells()
            elapse_time('after_update')
            root.after(100, periodic_service)
        
    buttons = []
    buttons.append(create_button(0, 0, 'help'))
    buttons.append(create_button(1, 0, 'demo'))
    buttons.append(create_button(2, 0, 'enter'))
    buttons.append(create_button(3, 0, 'run'))
    buttons.append(create_button(4, 0, 'reset'))
    canvas = create_canvas(5)

    for i in range(3):
        root.columnconfigure(i, weight=1)
        root.rowconfigure(i, weight=1)

    board.add_draw_board_callback(draw_board)
    board.add_periodic_callback(periodic_service)

def select_file(dir):
    from glob import glob
    paths = glob(dir + "*.mkv")
    filename = paths[0]
    return filename

class GameBoardModel:
    def __init__(self):
        self.x_tiles, self.y_tiles = 50, 50
        self.x_size, self.y_size = 500 // self.x_tiles, 500 // self.y_tiles        
        self.mode = None
        self._draw_callback = None
        self._periodic_callback = None
        self.cell_array_size = (self.x_tiles + 0) * (self.y_tiles + 0)
        self._cells = [0] * (self.cell_array_size)

    def reset(self, filename = 'conway.json'):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self._saved_cells = json.load(f)
                self._cells = self._saved_cells
                self._draw_board_callback(self._cells)
    
    def save_state(self):
        total = sum(self._cells)
        if total == 0:
            return
        self._saved_cells = copy.deepcopy(self._cells)
        with open('conway.json', 'w') as f:
            js = json.dumps(self._saved_cells)
            f.write(js)        
        
    def button_click(self, text):
        if self.mode == 'run' and text == 'run':
            text = 'stop'
        if self.mode == 'enter' and text != 'enter':
            self.save_state()
        self.mode = text
        if self.mode == 'run':
            self._periodic_callback()
        elif self.mode == 'help':
            print(help_string)
        elif self.mode == 'demo':
            self.demo()
        elif self.mode == 'reset':
            self.reset()
    
    def demo(self):
        from pathlib import Path
        from os import listdir
        from os.path import isfile, join
        path = Path('conway_demo')
        
        def get_files():
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            return onlyfiles
        
        def load_file(name):
            self.reset(join(path, name[0]))
            
        files = get_files()
        ListWindow(files, "select demo", load_file)
    
    def place_mark(self, col, row):
        if self.mode == 'enter':
            index = col * self.x_tiles + row
            self._cells[index] = 1 - self._cells[index]
            self._draw_board_callback(self._cells)
    
    def update_cells(self):
        from random import randint
        n = self.cell_array_size
        c = [0] * (self.cell_array_size)
        try:
            for x in range(0, self.x_tiles - 0):
                for y in range(0, self.y_tiles - 0):
                    index = y * self.x_tiles + x
                    v = self._cells[index]
                    s = sum([self._cells[(index + (k//3-1) * self.x_tiles + (k%3-1)) % n]
                             for k in range(9) if k != 4])
                    c[index] = (1 if s==3 or s==2 and v==1 else 0)
                    # Add rule: 1% chance of birth if only one neighbor
                    #c[index] = (1 if s==3 or s==2 and v==1 or 
                    #            s==1 and randint(0,100)//100 else 0)
        except Exception as e:
            print(e)
            raise(e)
        self._cells = c
        self._draw_board_callback(self._cells)
        
    def add_move_callback(self, callback):
        self._move_callbacks.append(callback)

    def add_draw_board_callback(self, callback):
        self._draw_board_callback = callback
        
    def add_periodic_callback(self, callback):
        self._periodic_callback = callback


if __name__ == "__main__":
    main()

