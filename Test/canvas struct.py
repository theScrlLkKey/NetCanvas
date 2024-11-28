import sys
import random  # colored static sometime


def fast_output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def output_canvas():
    pass  # update canvas using fastoutput, iterate through and parse into outputtable chars/locations


# setup canvas, fill with blanks, 40x100 canvas for now
canvas = []
for y in range(40):
    row = []
    for x in range(100):
        row.append("30")
    canvas.append(row)

print(canvas)

# rand color canvas
for y in range(40):
    for x in range(100):
        canvas[y][x] = str(random.randint(90, 97))

print(canvas)
