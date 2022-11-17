from tkinter import *
import requests
import json
import time
from datetime import datetime
import datetime as dt
from dateutil import parser
from math import sin, cos


win = Tk()
mtext = StringVar()


API_PATH = 'https://www.timeapi.io/api/Time/current/zone?timeZone=Europe/Moscow'

BG_COLOR = '#323133'
TEXT_COLOR = '#f5f6fa'

WIDTH = 150
HEIGHT = 50

XPOS = win.winfo_screenwidth() - 170
YPOS = win.winfo_screenheight() - 110

def init_window():
	win.title('Time Widget')
	win.geometry(f'{WIDTH}x{HEIGHT}+{XPOS}+{YPOS}')
	win.configure(bg='grey15')
	win.attributes('-topmost', True)
	win.attributes('-transparentcolor', 'grey15')
	win.overrideredirect(True)
	win.resizable(width=False, height=False)

	win.after(0, set_time)

def set_time():
	curtime = str((datetime.now() + dt.timedelta(0, delta)).time()).split('.')[0]
	mtext.set(curtime)
	win.after(1000, set_time)

def init_label():
	time_label = Label(win, textvariable=mtext, font=('Helvetica bold', 26), relief='flat',
		background=BG_COLOR, foreground=TEXT_COLOR, anchor='center') 
	time_label.pack(pady=20)
	time_label.place(relx=0.5, rely=0.5, anchor=CENTER)

def init_canvas():
	canvas = Canvas(win, width=WIDTH, height=HEIGHT, bg='grey15', highlightthickness=0)
	canvas.pack()

	return canvas

def roundPolygon(c, x1, y1, x2, y2, feather, res=5, **kwargs):
    points = []
    # top side
    points += [x1 + feather, y1,
               x2 - feather, y1]
    # top right corner
    for i in range(res):
        points += [x2 - feather + sin(i/res*2) * feather,
                   y1 + feather - cos(i/res*2) * feather]
    # right side
    points += [x2, y1 + feather,
               x2, y2 - feather]
    # bottom right corner
    for i in range(res):
        points += [x2 - feather + cos(i/res*2) * feather,
                   y2 - feather + sin(i/res*2) * feather]
    # bottom side
    points += [x2 - feather, y2,
               x1 + feather, y2]
    # bottom left corner
    for i in range(res):
        points += [x1 + feather - sin(i/res*2) * feather,
                   y2 - feather + cos(i/res*2) * feather]
    # left side
    points += [x1, y2 - feather,
               x1, y1 + feather]
    # top left corner
    for i in range(res):
        points += [x1 + feather - cos(i/res*2) * feather,
                   y1 + feather - sin(i/res*2) * feather]
        
    return c.create_polygon(points, **kwargs, smooth=TRUE)


date = parser.parse(json.loads(requests.get(API_PATH).text)['dateTime'])
pc_time = datetime.now()
delta = (date.replace(tzinfo=None) - pc_time.replace(tzinfo=None)).total_seconds()

init_window()
canvas = init_canvas()
init_label()

roundPolygon(canvas, 0, 0, WIDTH, HEIGHT, 8, fill=BG_COLOR)
win.mainloop()