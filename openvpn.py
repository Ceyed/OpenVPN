import subprocess
import sys
import PySimpleGUI as sg
import threading

ip = "146.0.75.211"
server_pin = "zgcHKBB+Owuaq4W+zBL1prdZBLDnn7mPrRryfXvea2A="
servers = {
    "Netherlands1" : "146.0.75.211",
    "Netherlands2" : "146.0.73.41"
}

def main():
    layout = [
                [sg.Text('Openconnect')],
                [sg.Button('Connect'), sg.Text(), sg.Button('Disconnect')],
                [sg.T('Server:', pad=((3,0),0)), sg.OptionMenu(values=(servers.keys()), key='server', auto_size_text=True)],
                [sg.Output(size=(60,15))],
                [sg.Button('Exit')]
             ]

    window = sg.Window('Openconnect v1', layout)
    while True:
        event, values = window.Read()
        if event in (None, 'Exit'):
            disconnect(window)
            exit
            break

        if event == 'Connect':
            t1 = threading.Thread(target=connect, args=(window,))
            t1.start()

        if event == 'Disconnect':
            disconnect(window)

    window.Close()

def connect(window, timeout=None):
    pre_command = """echo 'if(user.name()=="saeed")login();'|sudo -S echo ."""
    command = f"""echo 9288|sudo openconnect {ip} -u vbaz344043 --passwd-on-stdin --servercert pin-sha256:{server_pin}"""
    _ = subprocess.Popen(pre_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None
    retval = p.wait(timeout)
    return (retval, output)

def disconnect(window, timeout=None):
    # sudo killall openconnect
    command = "sudo killall openconnect"
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None
    retval = p.wait(timeout)
    return (retval, output)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error: " + str(e))
