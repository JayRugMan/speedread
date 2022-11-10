#! /usr/bin/env python3

import PySimpleGUIQt as sg
import os.path

sg.theme('DarkTeal12')  # See gui_theme_sampler.py for more options

# Window layout of 2 columns

file_list_column = [
  [
    sg.Text('Text File Folder'),sg.In(os.getcwd(), size=(25,1),
    enable_events=True, key='-FOLDER-'), sg.FolderBrowse(), sg.Stretch()
  ],
  [sg.Listbox(values=[], enable_events=True, size=(40,10), key='-FILE LIST-')],
  [
    sg.Slider(
      range=(1, 20), default_value=1, size=(20, 10), orientation='horizontal',
      enable_events=True, key="-SLIDER-", tooltip=("Adjust Words at a time")
    ),
    sg.Dial(
      range=(3,42), default_value=15, size=(10, 2), enable_events=True,
      key="-DIAL-", tooltip=("Adjust WPM")
    )
  ],
  [
    sg.Text('Words at a time:', justification='l'),
    sg.Text("1", key="-WORDS-"),
    sg.Text('Words per minute:', justification='r'),
    sg.Text("150", key="-WPM-")
  ],
  [sg.Dial(range=(1,14), size=(10, 2)), sg.Text("Some Words", justification='c')]
]

text_viewer_column = [
  [sg.Text("Choose a text file from the list on the left:")],
  [sg.Text(size=(40,1), key="-TOUT-")],
  [sg.Stretch(), sg.Image(key="-IMAGE-"), sg.Stretch(),]
]

# ---- full layout ----
layout = [
  [
    sg.Column(file_list_column),
    sg.VSeperator(),
    sg.Stretch(),
    sg.Column(text_viewer_column),
    sg.Stretch(),
  ]
]

window = sg.Window("Speed Read", layout, alpha_channel=0.9)

# the loop
while True:
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
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)
            window.VisibilityChanged()
        except:
            pass
    elif event == "-DIAL-":
      wpm = int(values["-DIAL-"]) * 10
      window["-WPM-"].update(wpm)
      window.VisibilityChanged()
    elif event == "-SLIDER-":
      wpm = int(values["-SLIDER-"])
      window["-WORDS-"].update(wpm)
      window.VisibilityChanged()

window.close()
    