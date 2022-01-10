"""A GUI program for openconnect"""

import threading
import PySimpleGUI as sg
from connection import connect, disconnect
import config

def main():
    """Main function for program"""
    sg.theme('Dark')
    layout = [
                [sg.Text('Openconnect', size=(22), justification='center', font=("Courier", 25))],
                [sg.Text('Server:', font=("Helvetica", 11), pad=((3,0),0)), \
                    sg.OptionMenu(values=(config.SERVERS.keys()), \
                        key='server', auto_size_text=True), \
                            sg.Button('Connect'), \
                                sg.Button('Disconnect', button_color=('white', 'red')), \
                                    sg.Button('Clear', button_color=('white', 'purple'))],
                [sg.Output(size=(60,15), key='output')],
                [sg.Button('Exit', size=(5, 1), font=("Courier", 12), \
                    button_color=('white', 'black'))]
             ]

    window = sg.Window('Openconnect v1', layout)
    while True:
        event, values = window.Read()
        if event in (None, 'Exit'):
            break

        if event == 'Connect':
            connect_threading = threading.Thread(target=connect, \
                args=(window, config.SERVERS[values['server']], config.SERVER_PIN))
            connect_threading.start()

        if event == 'Disconnect':
            disconnect(window)

        if event == 'Clear':
            window.FindElement('output').Update('')

    window.Close()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error: " + str(e))
