"""
Connection-related functions
"""

import subprocess
import sys

import config
from sort_server import sort_servers


def connect(window, values, timeout=None):
    """
    Connect function
    """

    # Disconnect incase it's already connected
    disconnect(window)

    # Select server for connection
    selected_server = values['server']
    if "Auto" in values['server'] or "[A]" in values['server']:
        # Finding fastest server
        print("Start sorting servers, Please be patient")
        selected_server = sort_servers()[0]

        # Update server list
        window.find_element('server').Update(\
            values=(["Auto [" + selected_server[:3] + ".." + selected_server[-1:] + "]"] + \
                list(config.SERVERS.keys())))
        window.find_element('server').Update(\
            "Auto [" + selected_server[:3] + ".." + selected_server[-1:] + "]")
        
        print("Sorting is done")

    ip = config.SERVERS[selected_server]

    # Start connecting proccess
    pre_command = """echo 'if(user.name()=="saeed")login();'|sudo -S echo ."""
    command = f"""echo 9288|sudo openconnect {ip} -u vbaz344043 --passwd-on-stdin --servercert pin-sha256:{config.SERVER_PIN}"""
    _ = subprocess.Popen(pre_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    prcss = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in prcss.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) \
            else 'backslashreplace').rstrip()
        output += line
        print(line)
        _ = window.Refresh() if window else None
    retval = prcss.wait(timeout)
    return (retval, output)

def disconnect(window, timeout=None):
    """
    Disconnect function
    """

    command = "sudo killall openconnect"
    prcss = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in prcss.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) \
            else 'backslashreplace').rstrip()
        output += line
        print(line)
        _ = window.Refresh() if window else None
    retval = prcss.wait(timeout)

    # Update server list
    window.find_element('server').Update(values=(["Auto"] + list(config.SERVERS.keys())))
    window.find_element('server').Update("Auto")

    return (retval, output)
