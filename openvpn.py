import os

ip = "146.0.73.41"
server_pin = "zgcHKBB+Owuaq4W+zBL1prdZBLDnn7mPrRryfXvea2A="
# servers = {
#     "Netherlands1" : "146.0.75.211",
#     "Netherlands2" : "146.0.73.41"
# }

pre_command = """echo 'if(user.name()=="saeed")login();'|sudo -S echo ."""
command = f"""echo 9288|sudo openconnect {ip} -u vbaz344043 --passwd-on-stdin --servercert pin-sha256:{server_pin}"""
_ = os.system(pre_command)
p = os.system(command)

print(p)
