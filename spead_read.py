#! /usr/bin/env python3

import PySimpleGUIQt as sg
import os.path
from os import system, name as os_name
from time import sleep         



working_dir = os.getcwd()
file_list = os.listdir(working_dir)
fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(working_dir, f))
            and f.lower().endswith((".txt"))
        ]
file_chosen = False
paused = False
opened = False


#====== Simple GUI stuff =======
sg.theme('DarkTeal12')  # See gui_theme_sampler.py for more options
font_1 = 'Any 12'
font_2 = 'Any 16'
font_button = 'Any 14'

file_works = [
  [
    sg.Text('Text File Folder', font=(font_1)),
    sg.In(
      working_dir,
      size=(45,1),
      enable_events=True,
      key='-FOLDER-',
      font=(font_1)
    ),
    sg.FolderBrowse(' Browse ', font=(font_button)),
    sg.Stretch()
  ],
  [sg.Text("")],
  [
    sg.Stretch(),
    sg.Listbox(
      values=fnames,
      enable_events=True,
      size=(65,10),
      key='-FILE LIST-',
      font=(font_1)
    ),
    sg.Stretch()
  ]
]

the_slider = [
  [
    sg.Stretch(),
    sg.Text('Words at a time:', justification='l', font=(font_1)),
    sg.Text("1", font=(font_1), key="-WORDS-"),
    sg.Stretch()
  ],
  [
    sg.Stretch(),
    sg.Slider(
      range=(1, 20), default_value=1, size=(35, 20), orientation='horizontal',
      enable_events=True, key="-SLIDER-", tooltip=("Adjust Words at a time")
    ),
    sg.Stretch()
  ]
]

the_dial = [
  [
    sg.Stretch(),
    sg.Text('Words per minute:', justification='r', font=(font_1)),
    sg.Text("150", font=(font_1), key="-WPM-"),
    sg.Stretch()
  ],
  [
    sg.Stretch(),
    sg.Dial(
      range=(3,64), default_value=15, size=(20, 4), enable_events=True,
      key="-DIAL-", tooltip=("Adjust WPM")
    ),
    sg.Stretch()
  ]
]

file_name = [
  [
    sg.Text(
      "(select a Text above and Click READ)",
      font=(font_1), key="-FILE NAME-"
    ),
    sg.Button(
      button_text=" READ ", font=(font_button),
      key="-READ-",enable_events=True
    ),
    sg.Button(
      button_text=" Pause/Play ", font=(font_button),
      key="-PAUSE-", enable_events=True
    ),
  ]
]

the_reader = [
  [
    sg.Text(
      "Click \"READ\"", justification='c', font=(font_2),
      enable_events=True, key="-READER-"
    )
  ]
]

# ---- full layout ----

layout = [
  [
    sg.Column(file_works)
  ],
  [
    sg.Stretch(), sg.Column(the_slider),
    sg.Stretch(),
    sg.Column(the_dial), sg.Stretch(),
  ],
  [
    sg.Stretch(), sg.Column(file_name), sg.Stretch()
  ],
  [sg.HSeperator()],
  [
    sg.Stretch(), sg.Column(the_reader), sg.Stretch()
  ]
]

window = sg.Window("Speed Read", layout, alpha_channel=0.9)

# the loop
while True:
    if opened and not paused:
        event, values = window.read(timeout=0)
        if last_word < len(words_list):
            to_display = ' '.join(words_list[first_word:last_word])
            ##JH window["-READER-"].update("{} {}".format(to_display, sleep_time))
            window["-READER-"].update(to_display)
            window.VisibilityChanged()
            sleep(sleep_time)
            first_word += w_count
            last_word += w_count
    else:
        event, values = window.read()
    if event in ("EXIT", sg.WIN_CLOSED):
        break
    # list files in the selected folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".txt"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the list
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-FILE NAME-"].update(filename)
            file_chosen = True
            ##JH window["-IMAGE-"].update(filename=filename)
            window.VisibilityChanged()
        except:
            pass
    elif event == "-SLIDER-":
        words = int(values["-SLIDER-"])
        window["-WORDS-"].update(words)
        window.VisibilityChanged()
    elif event == "-DIAL-":
        wpm = int(values["-DIAL-"]) * 10
        window["-WPM-"].update(wpm)
        window.VisibilityChanged()
    elif event == "-PAUSE-":
        if not paused:
            paused = True
        else:
            paused = False
    elif event == "-READ-":
        if file_chosen:
            with open(filename, 'r') as file:
                the_lines = [i for i in file.read().split('\n') if len(i) != 0]
            words_list = the_lines[0].split(' ')  # each word as list item\
            opened = True
            w_count = int(values["-SLIDER-"])
            wpm = int(values["-DIAL-"]) * 10
            first_word = 0
            last_word = w_count
            sleep_time = w_count / (wpm/60)
        


window.close()
    