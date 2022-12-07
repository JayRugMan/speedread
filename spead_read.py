#! /usr/bin/env python3

import PySimpleGUIQt as sg
import os.path
from os import system, name as os_name
from time import sleep         


def list_files(f_list, the_dir):
    fnames = [
                f
                for f in f_list
                if os.path.isfile(os.path.join(the_dir, f))
                and f.lower().endswith((".txt"))
            ]
    return fnames


def open_text(path_to_file):
    '''Opens file and returns a list of words'''
    with open(path_to_file, 'r') as file:
        the_lines = [i for i in file.read().split('\n') if len(i) != 0]
    w_list = the_lines[0].split(' ')  # each word as list item
    return w_list


working_dir = os.getcwd()
file_list = os.listdir(working_dir)
file_names = list_files(file_list, working_dir)
file_chosen = False
paused = True
loaded = False


#====== Simple GUI stuff =======
sg.theme('DarkBlue2')  # See gui_theme_sampler.py for more options
font_1 = 'Any 12'
font_2 = 'Any 16'
font_button = 'Any 14'

text_selection = [
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
      values=file_names,
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

button_panel = [
  [
    sg.Text(
      'No text selected',
      font=(font_1), key="-FILE NAME-"
    ),
    sg.Button(
      button_text=" Load ", font=(font_button),
      key="-LOAD-",enable_events=True
    ),
    sg.Button(
      button_text=" Play ", font=(font_button),
      key="-PLAY-", enable_events=True, disabled=True
    ),
    sg.Button(
      button_text=" Pause ", font=(font_button),
      key="-PAUSE-", enable_events=True, disabled=True
    ),
  ]
]

the_reader = [
  [
    sg.Text(
      'Select a text, word count, and wpm, then "Load"', justification='c', font=(font_2),
      enable_events=True, key="-READER-"
    )
  ]
]

# ---- full layout ----

layout = [
  [
    sg.Column(text_selection)
  ],
  [
    sg.Stretch(), sg.Column(the_slider),
    sg.Stretch(),
    sg.Column(the_dial), sg.Stretch(),
  ],
  [
    sg.Stretch(), sg.Column(button_panel), sg.Stretch()
  ],
  [sg.HSeperator()],
  [
    sg.Stretch(), sg.Column(the_reader), sg.Stretch()
  ]
]

window = sg.Window("Speed Read", layout, alpha_channel=0.9)

# the loop
while True:
    if loaded and not paused:
        event, values = window.read(timeout=0)

        if event in ("EXIT", sg.WIN_CLOSED):
            break
        elif event == "-PAUSE-":
            window["-PLAY-"].update(disabled=False)
            window["-PAUSE-"].update(disabled=True)
            paused = True
        elif last_word <= len(words_list):
            to_display = ' '.join(words_list[first_word:last_word])
            window["-READER-"].update(to_display)
            window.VisibilityChanged()
            sleep(sleep_time)
            first_word += w_count
            last_word += w_count
        else:
            window["-PLAY-"].update(disabled=False)
            window["-PAUSE-"].update(disabled=True)
            paused = True

    else:
        event, values = window.read()
        if event in ("EXIT", sg.WIN_CLOSED):
            break
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []
            file_names = list_files(file_list, folder)
            window["-FILE LIST-"].update(file_names)
        elif event == "-FILE LIST-":  # A file was chosen from the list
            try:
                filename = values["-FILE LIST-"][0]
                file_full_path = os.path.join(
                    values["-FOLDER-"], filename
                )
                window["-FILE NAME-"].update(filename)
                file_chosen = True
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
        elif event == "-LOAD-":
            if file_chosen:
                # creates list of words
                words_list = open_text(file_full_path)
                loaded = True
                w_count = int(values["-SLIDER-"])
                if w_count == 1:
                    word_gram = 'word'
                else:
                    word_gram = 'words'
                wpm = int(values["-DIAL-"]) * 10
                first_word = 0
                last_word = w_count
                sleep_time = w_count / (wpm/60)
                dis_str = "File Loaded for {} {} at {} WPM. Press Play!"
                to_display = dis_str.format(w_count, word_gram, wpm)
                window["-READER-"].update(to_display)
                window["-PLAY-"].update(disabled=False)
            else:
                the_text = 'Select a file before clicking that!'
                window["-FILE NAME-"].update(the_text)
        elif event == "-PLAY-":
            window["-PLAY-"].update(disabled=True)
            window["-PAUSE-"].update(disabled=False)
            paused = False
        


window.close()
    
