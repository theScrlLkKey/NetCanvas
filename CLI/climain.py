import sys
import random
import time
from pynput.keyboard import Listener, Key
import threading
import _thread


# move with arrow keys, 1-9 to cycle colors, space to set color. return cursor when done updating from server
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


def output_pixel(row=20, column=50, color="37", mode="solid", text="null", show_col=False):  # use for cursor and also individual pixel update
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
    # 1-5, q-t, a-g for primary colors, 6-0, y-p, h-; for secondary colors
    if key == Key.space:  # set color
        change_character(curs_y-1, curs_x-1, curs_color)  # -1 because curs_xy is terminal (index at 1) and canvas indexes at 0
    elif key == Key.shift:  # set color (secondary)
        change_character(curs_y - 1, curs_x - 1, curs_sec_color)
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
    output_pixel(1, canvas_cols+1, "37", "str", str(curs_y) + ", " + str(curs_x) + "  ")  # move to statusbar


def start_key_press():
    with Listener(on_press=on_press) as listener:
        listener.join()


fast_output("\033[2J")

canvas = []
canvas_rows = 40  # get these from server too
canvas_cols = 40
generate_canvas(canvas_rows, canvas_cols)  # for testing, gen canvas. canvas should be made on server, and synced here. connect to server instead.
output_canvas(canvas_rows, canvas_cols)

fast_output("\033[1;1H")  # calib cursor location
curs_x = 1
curs_y = 1

colors = [30,31,32,33,34,35,36,37,90,91,92,93,94,95,96,97]

curs_color = "33"
curs_sec_color = "90"

output_pixel(canvas_rows+1, 1, "37", "str", "<keybinds>")

key_press_sub = threading.Thread(target=start_key_press, args=())
key_press_sub.start()  # send updates here

while True:  # begin mainloop, get updates here
    output_canvas(canvas_rows, canvas_cols)   # get changed pixels and update those in canvas before redraw
    output_pixel(curs_y, curs_x, canvas[curs_y-1][curs_x-1], "trans")  # update virtual cursor, can't desync
    # statusbar: keybinds + cursor pos (placeholder) + bold current color/italic secondary color in keybinds
    time.sleep(0.1)
