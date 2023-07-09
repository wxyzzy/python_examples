#!/usr/bin/env python3
#
# Conway's game of life
# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
# James Nash
# built on framework from Henrik Tunedal
# Copyright 2023 Henrik Tunedal. Licensed under the MIT license.
#
# Points of interest:
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

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
from functools import partial

x_tiles, y_tiles = 20, 20
x_size, y_size = 500 // 20, 500 // 20

def main():
    root = tk.Tk()
    board = GameBoardModel()

    build_ui(root, board)

    root.title("Life")
    root.geometry("500x550")
    root.mainloop()


def build_ui(root, board):
    def on_button_click(col, row, text):
        board.button_click(text)
    
    def on_canvas_click(event):
        col, row = round(event.x//x_size), round(event.y//y_size)
        board.place_mark(col, row)

    def on_move(player, col, row):
        buttons[row * 3 + col].configure(text=player)

    def on_game_state_change(winner):
        showinfo(parent=root, title="Game over", message=f"Winner: {winner}")
        for b in buttons: b.configure(text="")
        board.reset()

    def create_button(col, row, text):
        b = ttk.Button(root, command=partial(on_button_click, col, row, text), text=text)
        b.grid(column=col, row=row, sticky="nw")
        return b
    
    def create_canvas():
        global line
        c = tk.Canvas(root, bg="white", height=500, width=500)
        c.grid(column=0, row=1, sticky='nw', columnspan=3)
        c.bind('<Button-1>', on_canvas_click)
        for i in range(100):
            line=c.create_line(0, i*y_size, 500, i*y_size, fill='#aaa')
            line=c.create_line(i*x_size, 0, i*x_size, 500, fill='#aaa')
        return c
    
    def draw_board(cells):
        for i in range(100):
            for j in range(100):
                coord = (i*x_size+1, j*y_size+1, i*x_size+x_size-3, j*y_size+y_size-3)
                fill = '#f00' if cells[i*x_tiles + j] == 1 else '#0f0'
                canvas.create_rectangle(coord, fill=fill, outline=fill)
    
    buttons = []
    buttons.append(create_button(0, 0, 'demo'))
    buttons.append(create_button(1, 0, 'enter'))
    buttons.append(create_button(2, 0, 'run'))
    canvas = create_canvas()

    for i in range(3):
        root.columnconfigure(i, weight=1)
        root.rowconfigure(i, weight=1)

    board.add_game_state_callback(draw_board)


class GameBoardModel:
    def __init__(self):
        self._mode = None
        self._game_state_callback = None
        self._cells = [0] * (x_tiles * y_tiles)

    def reset(self):
        self._state = BoardState()

    def button_click(self, text):
        self._mode = text
    
    def place_mark(self, col, row):
        if self._mode == 'enter':
            index = col * x_tiles + row
            self._cells[index] = 1 - self._cells[index]
            self._game_state_callback(self._cells)
    
    def add_move_callback(self, callback):
        self._move_callbacks.append(callback)

    def add_game_state_callback(self, callback):
        self._game_state_callback = callback


if __name__ == "__main__":
    main()

