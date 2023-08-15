import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from matplotlib.animation import FuncAnimation
from matplotlib import animation
from itertools import count
import csv
from matplotlib.widgets import Cursor

plt.style.use('fivethirtyeight')

line_cnt = 0
maxi=-0.000000001
mini=1000000000
symbol=input("symbol name:")
date=str(datetime.today())[0:11]

time_frame=input("enter the time frame in seconds/minutes/hours:")
location=input("enter the location where you want to store:")

time_stamp=0

if 'minutes' in time_frame:
    time_stamp=int(float(time_frame[:-8])*60)
    print('minutes')
elif 'hours' in time_frame:
    time_stamp=int(float(time_frame[:-8])*3600)
    print('hours')
else:
    time_stamp=int(time_frame[:-8]) #in seconds
    print('seconds')

while(length<time_stamp):
    with open(location + "/RTTS/{}.txt".format(symbol), 'r') as file:
        t = file.readlines()
        length = len(t)

time_frame='{}_seconds'.format(time_stamp)

start=True
start_hour=0
start_minute=0
start_second=0
x_start=0

current_annotation=None

count=-1

with open(location + '/RTTS/{}.csv'.format(symbol),'a',newline="") as file:
    writer=csv.writer(file)
    writer.writerow(['date','time','O','H','L','C'])

cursor = Cursor(ax=plt.gca(), horizOn=True, vertOn=True, color='black', linewidth=1, linestyle='dotted',useblit=True)

def curr_time(x):
    global time_stamp,start_hour,start_second,start_minute

    total_seconds=x*time_stamp
    hour_conversion = int(total_seconds/ 3600)
    minute_coverion = int((float(total_seconds/ 3600) - hour_conversion) * 60)
    second_conversion = int((float((float(total_seconds/ 3600) - hour_conversion) * 60) - minute_coverion) * 60)

    curr_second = start_second + second_conversion
    curr_minute = start_minute + minute_coverion + int(curr_second/60)
    curr_hour=start_hour + hour_conversion + int(curr_minute/60)

    curr_hour=curr_hour%12
    curr_second=curr_second%60
    curr_minute=curr_minute%60

    t=str(curr_hour) + ':' + str(curr_minute) + ':' + str(curr_second)
    # t=curr_hour + curr_minute/100 + curr_second/10000

    return t

def update_annotation(x,y):
    global current_annotation,time_stamp

    t=curr_time(x)
    # Remove the current annotation if it exists so that previous annotations are removed
    if current_annotation!=None :
        current_annotation.remove()

    #making the anotation
    # arrow_props = dict(facecolor='black', edgecolor='black', arrowstyle='->')
    current_annotation = plt.annotate(f'{t}, {y:.2f}', (x, y),textcoords="offset points", xytext=(0, 10),ha='center', va='bottom', color='black')

    plt.gcf().canvas.draw()


def on_click(event):
    if event.inaxes is not None: # this condition is to check if we have clicked inside the grpah or not
        x_clicked = event.xdata
        y_clicked = event.ydata
        update_annotation(x_clicked, y_clicked)

        # plt.annotate(f'y={y_clicked:.2f}', (x_clicked, y_clicked),
        #              textcoords="offset points", xytext=(0, 10), ha='center', color='black')
        # plt.gcf().canvas.draw()

def animate(i):
    global line_cnt,maxi,symbol,mini,start,x_start,cursor,time_stamp,bar_width,count,start_minute,start_hour,start_second

    count+=1

    y = np.array([])

    # because we are also clearing the data from the text file if it exceeds 960 rows therefore to avoid any error
    while(length<time_stamp):
        with open(location + "/RTTS/{}.txt".format(symbol), 'r') as file:
        t = file.readlines()
        length = len(t)
    
    with open(location + '/RTTS/{}.txt'.format(symbol), 'r') as file:
        t = file.readlines()
        print(len(t))
        t = t[-time_stamp: len(t)]
        # t=t[line_cnt:line_cnt+time_stamp]
        for i in t:
            i = float(i[:-1])
            y = np.append(y,i)


    time = datetime.now().strftime('%H:%M:%S')
    hour = time[0:2]
    minute = time[3:5]
    second = time[6:8]

    if(start):
        start_hour=int(hour)
        start_minute=int(minute)
        start_second=int(second)
        start=False

    # x = float(hour + '.' + minute+second)
    # # x=float('0.'+minute)
    # if start:
    #     x_start=x
    #     start=False

    x=count

    cursor.set_active(True)  # Activate the cursor
    # cursor.set_xdata(x)
    plt.gcf().canvas.mpl_connect('button_press_event', on_click)

    H = np.max(y)
    L = np.min(y)
    O = y[0]
    C = y[-1]

    if(H>maxi):
        maxi=H
    if(L<mini):
        mini=L

    # plt.gca().clear()

    print(O,H,L,C)

    if O < C:
        plt.vlines(x, L, H, color='green',linewidth=0.7)
        plt.bar(x, O - C, width=0.6, bottom=O, color='green')

    else:
        t=C-O
        if C==O:
            t=0.3
        plt.vlines(x, L, H, color='red',linewidth=0.7)
        plt.bar(x, t, width=0.6, bottom=C, color='red')


    plt.ylim(mini-1,maxi+1)

    if(count>=180):
        plt.xlim(count-178, count+2)
    else :
        plt.xlim(-1,count+5)
    plt.xlabel("time")
    plt.ylabel('Price')


    plt.title('                                                   {}                 O {} H {} L {} C {}'.format(symbol,O,H,L,C))

    with open(location + '/RTTS/{}({}).csv'.format(symbol,time_frame),'a',newline="") as file:
        writer=csv.writer(file)
        writer.writerow([date,time,O,H,L,C])

    line_cnt +=time_stamp

anim = FuncAnimation(plt.gcf(), animate, cache_frame_data=False, interval=time_stamp*1000)

# matplotlib.rcParams['animation.ffmpeg_path']='C:\\Users\\bbeha\\Desktop\\ffmpeg\\ffmpeg-6.0-essentials_build\\bin\\ffmpeg.exe'
# # writer =animation.FFMpegWriter(fps=30,bitrate=1800)
# anim.save('C:/Users/bbeha/Desktop/RTTS/{}_chart.mp4'.format(symbol))

plt.show()
