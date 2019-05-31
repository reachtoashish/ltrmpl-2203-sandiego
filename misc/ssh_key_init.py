import getpass
import sys
import telnetlib
import time
import datetime

ios_config = """
conf t
crypto key generate rsa
yes
2048
exit
exit
"""

xe_config = """
conf t
crypto key generate rsa
yes
2048
"""

xr_config = """
crypto key generate rsa
yes
2048
exit
"""

rr_config = """
conf t
router bgp 1
 address-family vpnv4 unicast
 !
root
commit
exit
exit
"""

rr2_config = """
conf t
router bgp 1
 !
 neighbor 192.168.0.1
  remote-as 1
  update-source Loopback0
  address-family vpnv4 unicast
   route-policy PASS in
   route-reflector-client
   route-policy PASS out
  !
 !
 neighbor 192.168.0.4
  remote-as 1
  update-source Loopback0
  address-family vpnv4 unicast
   route-policy PASS in
   route-reflector-client
   route-policy PASS out
  !
 !
root
commit
exit
exit
"""

pe4_config = """
conf t
route-policy PASS
  pass
end-policy
!
 !
root
commit
exit
exit
"""


def log_info(message_string):
    # print message_string
    ts = time.gmtime()
    timestamp = time.strftime("%c", ts)
    log_message = timestamp + " UTC   :   " + message_string + "\n"
    print log_message
    with open('log_file.txt', 'a') as log_file:
        log_file.write(log_message)


def login_router(tn, user, password):
    tn.read_until("Username: ")
    tn.write(user + "\n")
    log_info("username entered")
    if password:
        tn.read_until("Password: ")
    tn.write(password + "\n")
    log_info('password entered')
    tn.read_until("#")
    return tn


def read_output(tn, command):
    # print ("entering command %s" % command)
    tn.write(command + "\n")
    tn.write("!End command" + "\n")
    return tn.read_until("!End command")


IOS_HOST = ["198.18.1.111", "198.18.1.112"]
XE_HOST = ["198.18.1.12"]
XR_HOST = ["198.18.1.11", "198.18.1.13", "198.18.1.14", "198.18.1.100", "198.18.1.200"]
RR_HOST = ["198.18.1.100", "198.18.1.200"]

# user = raw_input("Enter your remote account: ")
# password = getpass.getpass()

user = "cisco"
password = "cisco"

for HOST in IOS_HOST:
    telnet_obj = telnetlib.Telnet(HOST)
    post_login = login_router(telnet_obj, user, password)
    post_login.write(ios_config + "\n")
    log_info('Key generated for Host: %s' % HOST)
    time.sleep(5)

for HOST in XE_HOST:
    telnet_obj = telnetlib.Telnet(HOST)
    post_login = login_router(telnet_obj, user, password)
    post_login.write(xe_config + "\n")
    log_info('Key generated for Host: %s' % HOST)
    post_login.write("no netconf-yang" + "\n")
    log_info('netconf deleted for Host: %s' % HOST)
    time.sleep(5)
    post_login.write("netconf-yang" + "\n")
    post_login.write("yes" + "\n")
    log_info('netconf configured for Host: %s' % HOST)
    post_login.write("exit" + "\n")
    post_login.write("exit" + "\n")
    
for HOST in XR_HOST:
    telnet_obj = telnetlib.Telnet(HOST)
    post_login = login_router(telnet_obj, user, password)
    post_login.write(xr_config + "\n")
    log_info('Key generated for Host: %s' % HOST)
    if HOST == "198.18.1.14":
        time.sleep(5)
        telnet_obj = telnetlib.Telnet(HOST)
        post_login = login_router(telnet_obj, user, password)
        post_login.write(pe4_config + "\n")
        log_info('PE4 specific route-policy pre config pushed: %s' % HOST)
    time.sleep(5)

for HOST in RR_HOST:
    telnet_obj = telnetlib.Telnet(HOST)
    post_login = login_router(telnet_obj, user, password)
    post_login.write(rr_config + "\n")
    log_info('RR BGP pre config pushed: %s' % HOST)
    if HOST == "198.18.1.200":
        time.sleep(5)
        telnet_obj = telnetlib.Telnet(HOST)
        post_login = login_router(telnet_obj, user, password)
        post_login.write(rr2_config + "\n")
        log_info('RR2 specific BGP pre config pushed: %s' % HOST)
    time.sleep(5)

