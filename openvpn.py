"""
A GUI program for openconnect
"""

import threading

import PySimpleGUI as sg

import config
from connection import connect, disconnect


def main():
    """
    Main function for program
    """

    # Setting up theme and layouts of window
    sg.theme('Dark')
    layout = [
                [sg.Text('Openconnect', size=(22), justification='center', font=("Courier", 25))],
                [sg.Text('Server:', font=("Helvetica", 11), pad=((3,0),0)), \
                    sg.OptionMenu(values=(["Auto"] + list(config.SERVERS.keys())),
                        default_value="Auto", \
                            key='server', auto_size_text=True), \
                                sg.Button('Connect'), \
                                    sg.Button('Disconnect', button_color=('white', 'red')), \
                                        sg.Button('Clear', button_color=('white', 'purple'))],
                [sg.Output(size=(60,15), key='output')],
                [sg.Button('Exit', size=(5, 1), font=("Courier", 12), \
                    button_color=('white', 'black'))]
             ]

    window = sg.Window('Openconnect v1.1', layout)
    while True:
        event, values = window.Read()

        # 'Exit' button clicked
        if event in (None, 'Exit'):
            break

        # 'Connect' button clicked
        if event == 'Connect':
            # Connect to selected/fastest server
            connect_threading = threading.Thread(target=connect, \
                args=(window, values))
            connect_threading.start()

        # 'Disconnect' button clicked
        if event == 'Disconnect':
            disconnect(window)

        # 'Clear' button clicked
        if event == 'Clear':
            window.find_element('output').Update('')

    window.Close()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error: " + str(e))
