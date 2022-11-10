#! /usr/bin/env python3
## Credits:
## https://www.pysimplegui.org/en/latest/cookbook/#the-demo-programs-are-also-recipes

import PySimpleGUIQt as sg

"""
    Allows you to "browse" through the Theme settings.  Click on one and you'll see a
    Popup window using the color scheme you chose.  It's a simple little program that also demonstrates
    how snappy a GUI can feel if you enable an element's events rather than waiting on a button click.
    In this program, as soon as a listbox entry is clicked, the read returns.
"""

sg.theme('DarkTeal12')


layout = [[sg.Text('Theme Sampler')],
          [sg.Text('Click a Theme color to see demo window')],
          [sg.Listbox(values=sg.theme_list(), size=(20, 12), key='-LIST-', enable_events=True)],
          [sg.Stretch(), sg.Button(' Exit ')]]

window = sg.Window('Theme Sampler', layout)

while True:  # Event Loop
    event, values = window.read()
    if event in (sg.WIN_CLOSED, ' Exit '):
        break
    try:
        sg.theme(values['-LIST-'][0])
    except TypeError:
        pass
    except IndexError:
        pass
    try:
        sg.popup_get_text('This is {}'.format(values['-LIST-'][0]), location=(700,500))
    except TypeError:
        pass
    except IndexError:
        pass

window.close()