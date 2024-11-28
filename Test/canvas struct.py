import sys
import random  # colored static sometime


def fast_output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def output_canvas():
    pass  # update canvas using fastoutput, iterate through and parse into outputtable chars/locations

def generateNewCanvas(rows=40,columns=100):
    # setup canvas, fill with blanks, 40x100 canvas for now
    global canvas = []
    for y in range(rows):
        row = []
        for x in range(columns):
            row.append("30")
    canvas.append(row)

def randomizeCanvas()
    # rand color canvas
    for y in range(40):
        for x in range(100):
            global canvas[y][x] = str(random.randint(90, 97))

print(canvas)
canvas[3][3] = "h"
print(canvas[3][3])