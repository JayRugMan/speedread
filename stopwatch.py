#! /usr/bin/env python3

import PySimpleGUIQt as sg
from datetime import datetime, timedelta


class timer():
    '''This object will keep the time'''
 
    def __init__(self):
        self.started = False
        self.paused = False
        self.time_mark = datetime.now()
        self.clock_time = timedelta(0)
        self.show = "0:00:00.000000"
    
    def start(self):
        self.time_mark = datetime.now()
        if self.paused:
            self.paused = False
        self.started = True

    def stop(self):
        self.paused = True
    
    def update(self):
        now = datetime.now()
        self.clock_time += (now - self.time_mark)
        self.time_mark = now
        self.show = str(self.clock_time)


the_timer = timer()

sg.theme('BlueMono')  # See gui_theme_sampler.py for more options
font_1 = 'Any 16'
font_button = 'Any 14'

layout = [
    [
        sg.Stretch(),
        sg.Text(
            the_timer.show, font=(font_1), key="-CLOCK-"
        ),
        sg.Stretch(),
    ],
    [
        sg.Stretch(),
        sg.Button(
            button_text=" start ", font=(font_button),
            key="-START-", enable_events=True
        ),
        sg.Stretch(),
        sg.Button(
            button_text=" stop ", font=(font_button),
            key="-STOP-", enable_events=True
        ),
        sg.Stretch(),
        sg.Button(
            button_text=" reset ", font=(font_button),
            key="-RESET-", enable_events=True
        ),
    ]
]

window = sg.Window("Stop Watch", layout, alpha_channel=0.9)

# the loop
while True:
    if the_timer.started and not the_timer.paused:
        event, values = window.read(timeout=10)
        if event in ("EXIT", sg.WIN_CLOSED):
            break
        elif event == '-STOP-':
            the_timer.stop()
            pass
        else:
            the_timer.update()
            window["-CLOCK-"].update(the_timer.show)
    else:
        event, values = window.read()
        if event in ("EXIT", sg.WIN_CLOSED):
            break
        if event == '-START-':
            the_timer.start()
        elif event == '-RESET-':
            the_timer = timer()
            window["-CLOCK-"].update(the_timer.show)


window.close()
    