#! /usr/bin/env python3

import PySimpleGUIQt as sg
from datetime import datetime, timedelta


class timer():
    '''This object will keep the time'''
 
    def __init__(self):
        self.started = False
        self.paused = False
        self.time_mark = datetime.now()
        self.clock_time = timedelta(0)  # this will acumulate in the update method
        self.show = "0:00:00.000000"
    
    def start(self):
        '''Sets initial time mark, initial start or unpause'''
        self.time_mark = datetime.now()
        if self.paused:
            self.paused = False
        if not self.started:
            self.started = True

    def stop(self):
        '''Pauses the timer - freezes the time on the display'''
        self.paused = True
    
    def update(self):
        '''Adds time to the clock time'''
        now = datetime.now()  # snapshots now for use in clock-time delta and time mark
        self.clock_time += (now - self.time_mark)  # adds time diff to clock time
        self.time_mark = now  # resets time mark
        self.show = str(self.clock_time)  # displays as hh:mm:ss.ssssss


the_timer = timer()

sg.theme('DarkGrey5')  # See gui_theme_sampler.py for more options
font_1 = 'Any 16'
font_button = 'Any 14'

'''
       -CLOCK-
-START- -STOP- -RESET-
'''
layout = [
    [
        sg.Stretch(),
        sg.Text(  # main time display
            the_timer.show, font=(font_1), key="-CLOCK-"
        ),
        sg.Stretch(),
    ],
    [
        sg.Stretch(),
        sg.Button(  # start button
            button_text=" start ", font=(font_button), key="-START-"
        ),
        sg.Stretch(),
        sg.Button(  # stop button
            button_text=" stop ", font=(font_button), key="-STOP-"
        ),
        sg.Stretch(),
        sg.Button(  # reset button
            button_text=" reset ", font=(font_button), key="-RESET-"
        ),
        sg.Stretch()
    ]
]

window = sg.Window("Stop Watch", layout, alpha_channel=0.9)

# the loop
while True:
    if the_timer.started and not the_timer.paused:
        # This will only run when start has been
        # pressed and until stop or exit is pressed
        event, values = window.read(timeout=1)  # only waits 10 ms for input
        if event in ("EXIT", sg.WIN_CLOSED):
            break  # necessary for window and program to close properly
        elif event == '-STOP-':
            the_timer.stop()  # sets paused to true
            pass
        else:
            the_timer.update()  # updated every 10 milliseconds if no input
            window["-CLOCK-"].update(the_timer.show)
    else:
        # start and reset do nothing wile time is started (running)
        # these events only work if not started or paused
        event, values = window.read()  # wait indefinitely for input from window
        if event in ("EXIT", sg.WIN_CLOSED):
            break  # necessary for window and program to close properly
        if event == '-START-':
            the_timer.start()  # sets started to true and paused to false
        elif event == '-RESET-':
            the_timer = timer()  # fresh timer class set
            window["-CLOCK-"].update(the_timer.show)


window.close()  # necessary for window and program to close properly
    
