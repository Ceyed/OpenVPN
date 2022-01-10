"""Connection-related functions"""

import subprocess
import sys

def connect(window, vpn_ip, server_pin, timeout=None):
    """Connect function"""
    pre_command = """echo 'if(user.name()=="saeed")login();'|sudo -S echo ."""
    command = f"""echo 9288|sudo openconnect {vpn_ip} -u vbaz344043 --passwd-on-stdin --servercert pin-sha256:{server_pin}"""
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
    """Disconnect function"""
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
    return (retval, output)
