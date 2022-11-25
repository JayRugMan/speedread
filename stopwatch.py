#! /usr/bin/env python3

import PySimpleGUIQt as sg
from datetime import datetime
from datetime import timedelta


class timer():
    '''This object will keep the time'''
 
    def __init__(self):
        self.started = False
        self.paused = False
        self.beginning = 0
        self.show = "0:00:00.000000"
    
    def start(self):
        if self.paused:
            self.paused = False
        if not self.started:
            self.beginning = datetime.now()
        self.started = True

    def stop(self):
        self.paused = True
    
    def update(self):
        now = datetime.now()
        new_delta = now - self.beginning
        self.show = str(new_delta)


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
            key="-STOP-"
        ),
        sg.Stretch(),
        sg.Button(
            button_text=" reset ", font=(font_button),
            key="-RESET-"
        ),
    ]
]

window = sg.Window("Stop Watch", layout, alpha_channel=0.9)

# the loop
while True:
    if the_timer.started and not the_timer.paused:
        event, values = window.read(timeout=0)
        the_timer.update()
        window["-CLOCK-"].update(the_timer.show)
        window.VisibilityChanged()
    else:
        event, values = window.read()
    if event in ("EXIT", sg.WIN_CLOSED):
        break
    # list files in the selected folder
    if event == '-START-':
        the_timer.start()
    elif event == '-STOP-':
        the_timer.stop()
    elif event == '-RESET-':
        the_timer = timer()
        window["-CLOCK-"].update(the_timer.show)


window.close()
    