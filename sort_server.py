import platform
import re
import subprocess
from traceback import print_tb

import config


def sort_servers():
    """
    Sorting servers
    """

    def ping(host):
        """
        ping to given server
        """

        # Creating command
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '3', host]

        try:
            # Finding ping response if possible
            res = (subprocess.check_output(command)).decode()
            pings = []
            for resu in res.split("\n"):
                x = re.findall("time=.+ ms", resu)
                if x:
                    pings.append(int(x[0][5:-3]))
            if len(pings) < 3:
                for _ in 3-len(pings):
                    pings.append(999.9)
        except:
            # If can't get ping response
            pings = [
                999.9,
                999.9,
                999.9
            ]
        # Getting average of 3 ping responses
        return sum(pings) / len(pings)


    # Getting server's speeds (pings)
    pings = []
    for server in config.SERVERS:
        pings.append([server, ping(config.SERVERS[server])])
        print(".", end="")
    print()

    # Sorting servers from fastest to slowest
    pings.sort(key=lambda x: x[1])

    # Extract servers's names (fastest to slowest)
    sorted_servers = []
    for item in pings:
        sorted_servers.append(item[0])

    # Returning sorted servers's names
    return sorted_servers
