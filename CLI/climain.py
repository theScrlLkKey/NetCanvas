import sys
import random
import time
from pynput.keyboard import Listener, Key
import threading
import _thread


# all terminal stuff is offset by one, ensure canvas stays indexed at zero


def fast_output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def output_canvas(rows=40, columns=100):
    # update canvas using fastoutput, iterate through and parse into outputtable chars/locations
    output_str = ""
    for y in range(rows):
        for x in range(columns):
            output_str += f"\033[{y+1};{(x*2)+1}H"  # +1 because terminal indexes at 1 not 0
            output_str += f"\033[{canvas[y][x]}m██"
        output_str += "\n"
    fast_output(output_str)


def output_pixel(row=20, column=50, color="37", mode="solid", text="null", show_col=False):  # use for cursor and individual pixel update
    if mode == "solid":
        fast_output(f"\033[{row};{(column*2)-1}H\033[{color}m██")  # -1 because terminal indexes at 1
    elif mode == "trans":
        if show_col:
            fast_output(f"\033[{row};{(column * 2) - 1}H\033[{color}m▒\033[{curs_color}m▒")
        else:
            fast_output(f"\033[{row};{(column * 2) - 1}H\033[{color}m▒▒")
    elif mode == "str":
        fast_output(f"\033[39m\033[{row};{(column*2)-1}H\033[{color}m{text}")


def generate_canvas(rows=40, columns=100):
    # setup canvas, fill with blanks, 40x100 canvas for now
    global canvas
    for y in range(rows):
        row = []
        for x in range(columns):
            row.append("90")
        canvas.append(row)


def randomize_canvas(rows=40, columns=100):
    # rand color canvas
    global canvas
    for y in range(rows):
        for x in range(columns):
            canvas[y][x] = str(colors[random.randint(0, 15)])


def change_character(row=20, column=50, color="37"):
    canvas[row][column] = color
    # pixel send code here


def on_press(key):
    global curs_x
    global curs_y
    global curs_color
    # 1-4, q-r, a-f, z-v for direct draw, 5-8, t-i, g-k, b-, for primary draw
    if hasattr(key, 'char'):
        key_color = str(key.char)
        # right keyboard palette sets spacebar color, shift is color picker, left keyboard palette directly draws
        if key_color in set_color_key_dict:
            curs_color = colors[set_color_key_dict[key_color]]
        elif key_color in dir_color_key_dict:
            change_character(curs_y - 1, curs_x - 1, colors[dir_color_key_dict[key_color]])
    elif key == Key.space:  # set color
        change_character(curs_y-1, curs_x-1, curs_color)  # -1 because curs_xy is terminal (index at 1) and canvas indexes at 0
    elif key == Key.shift:  # color picker
        curs_color = canvas[curs_y - 1][curs_x - 1]
    elif key == Key.left:
        if curs_x > 1:
            curs_x -= 1
    elif key == Key.right:
        if curs_x < canvas_cols:
            curs_x += 1
    elif key == Key.up:
        if curs_y > 1:
            curs_y -= 1
    elif key == Key.down:
        if curs_y < canvas_rows:
            curs_y += 1
    elif key == Key.home:
        fast_output("\033[2J ")
        _thread.interrupt_main()
        exit()
    output_pixel(1, canvas_cols+1, "37", "str", str(curs_y) + ", " + str(curs_x) + "  ")  # todo: display in statusbar


def start_key_press():
    with Listener(on_press=on_press) as listener:
        listener.join()


fast_output("\033[2J")  # clear screen

# various defines
canvas = []

colors = [30, 31, 32, 33, 34, 35, 36, 37, 90, 91, 92, 93, 94, 95, 96, 97]
# grays, rgby, m and c
# 1-4, q-r, a-f, z-v for primary colors, 5-8, t-i, g-k, b-, for secondary colors
# this is a good idea and very readable (better than ifs)
dir_color_key_dict = {"1":0, "2":8, "3":7, "4":15, "q":1, "a":9, "w":2, "s":10, "e":4, "d":12, "r":3, "f":11, "z":5, "x":13, "c":6, "v":14}
set_color_key_dict = {"5":0, "6":8, "7":7, "8":15, "t":1, "g":9, "y":2, "h":10, "u":4, "j":12, "i":3, "k":11, "b":5, "n":13, "m":6, ",":14}

combined_color_key_dict = dir_color_key_dict.copy()  # Combines the two dictionaries into one (why? - scrl)
for key, val in dict.items(set_color_key_dict):
    combined_color_key_dict[key] = val

# initial starting colors in ansi codes
curs_color = "33"

# create statusbar static bits - print color blocks, primary keys below, secondary below - arrange in grid?
# make placeholder for coords, figure out bold/italic? server status? programatically generate keybinds, and update? hm, cpu time
# also, move to the right side of screen, not bottom
status_fstring = f"""1 2 3 4  q a  w s  e d  r f  z x  c v
5 6 7 8  t g  y h  u j  i k  b n  m ,
1, 1                         offline"""

# status_fstring += "\n"  # made this code work, moved it to a better spot. unsure if this is the best way to print out keybinds...
# for key, val in dict.items(combined_color_key_dict):
#     status_fstring += "\033[39m" + str(key) + " "
# status_fstring += "\n"
# for key, val in dict.items(combined_color_key_dict):
#     status_fstring += f"\033[{colors[val]}m██" + " "

# for testing, generate canvas. once server made, connect and get canvas, then output it. no need to generate
canvas_rows = 40  # get these from server too
canvas_cols = 40
generate_canvas(canvas_rows, canvas_cols)
output_canvas(canvas_rows, canvas_cols)

fast_output("\033[1;1H")  # calib cursor location
curs_x = 1
curs_y = 1

key_press_sub = threading.Thread(target=start_key_press, args=())
key_press_sub.start()  # send updates here

while True:  # begin mainloop, get updates here
    output_canvas(canvas_rows, canvas_cols)   # get changed pixels and update those in canvas before redraw
    output_pixel(curs_y, curs_x, canvas[curs_y-1][curs_x-1], "trans")  # update virtual cursor, can't desync
    # todo: statusbar: keybinds + cursor pos (placeholder of 1,1) + bold current color/italic secondary color in keybinds (how?)
    output_pixel(canvas_rows + 1, 1, "37", "str", status_fstring)
    time.sleep(0.05)
