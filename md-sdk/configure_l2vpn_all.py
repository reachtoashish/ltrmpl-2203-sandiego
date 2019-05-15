import argparse
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_l2vpn_cfg as l2vpn_xr_cfg
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native as xe_native
from ydk.types import Empty
import logging
import re
import sys

log = logging.getLogger('ydk')
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
log.addHandler(handler)

def configure_l2vpn_xr(l2vpn_obj, remote_ip_address, intf_name, pw_id, pw_name):
    '''Configure XConnect on PE device'''
    xconnectGroup = l2vpn_obj.Database.XconnectGroups.XconnectGroup()
    xconnectGroup.name = pw_name
    p2pXconnect = xconnectGroup.P2pXconnects.P2pXconnect()
    p2pXconnect.name = "p2p-ciscolive"
    pwid = p2pXconnect.Pseudowires.Pseudowire()
    pwid.pseudowire_id = int(pw_id)
    neighbor = pwid.Neighbor()
    neighbor.neighbor = remote_ip_address
    pwid_ac = p2pXconnect.AttachmentCircuits.AttachmentCircuit()
    pwid_ac.name = intf_name
    pwid.neighbor.append(neighbor)
    p2pXconnect.attachment_circuits.attachment_circuit.append(pwid_ac)
    p2pXconnect.pseudowires.pseudowire.append(pwid)
    xconnectGroup.p2p_xconnects.p2p_xconnect.append(p2pXconnect)
    l2vpn_obj.database.xconnect_groups.xconnect_group.append(xconnectGroup)


def configure_l2vpn_xe(l2vpn_xe_obj, remote_ip_address, intf_name, pw_id, pw_name):
    intf_name_fnd = re.search(r".*(\d+\.\d+)", intf_name)
    if intf_name_fnd:
        intf = l2vpn_xe_obj.Interface.GigabitEthernet()
        intf.name = intf_name_fnd.group(1)
    else:
        print("Invalid interface name entered for XE device.")
        sys.exit()
    intf_encap = intf.Encapsulation()
    intf_encap_dot1q = intf_encap.Dot1Q()
    intf_encap_dot1q.vlan_id = int(pw_id)  # making vlan_id = pw_id
    xe_xconnect = intf.Xconnect()
    xe_xconnect.address = remote_ip_address
    xe_xconnect.vcid = int(pw_id)
    xe_xconnect_encap = xe_xconnect.Encapsulation()
    xe_xconnect.encapsulation = xe_xconnect_encap.mpls
    intf.xconnect = xe_xconnect
    intf_encap.dot1q = intf_encap_dot1q
    intf.encapsulation = intf_encap
    l2vpn_xe_obj.interface.gigabitethernet.append(intf)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pe1_ip', nargs='?', help="IP address of PE1")
    parser.add_argument('--pe1_platform', nargs='?', default="IOSXE", help="PE1 Platform")
    parser.add_argument('--pe1_intf', nargs='?', help="Interface of PE1")
    parser.add_argument('--pe2_ip', nargs='?', help="IP address of PE2")
    parser.add_argument('--pe2_platform', nargs='?', default="IOSXR", help="PE2 Platform")
    parser.add_argument('--pe2_intf', nargs='?', help="Interface of PE2")
    parser.add_argument('--pw_id', nargs='?', help="Pseudo-wire ID")
    parser.add_argument('--pw_name', nargs='?', default="ciscolive", help="Pseudo-wire XConnect Name")
    parser.add_argument('--username', nargs='?', default="cisco", help="Username")
    parser.add_argument('--password', nargs='?', default="cisco", help="Password")
    args = parser.parse_args()
    cisco_devices = [{"ip_address":args.pe1_ip,
                      "platform" : args.pe1_platform,
                      "intf_name":args.pe1_intf,
                      "dest_ip":args.pe2_ip},
                     {"ip_address":args.pe2_ip,
                      "platform": args.pe2_platform,
                      "intf_name":args.pe2_intf,
                      "dest_ip":args.pe1_ip}]
    for cisco_device in cisco_devices:
        pe_ip_address = cisco_device["ip_address"]
        intf_name = cisco_device["intf_name"]
        remote_ip_address = cisco_device["dest_ip"]


        crud = CRUDService()
        
        if cisco_device["platform"] == "IOSXE":
            provider = NetconfServiceProvider(address=pe_ip_address, port=830, username=args.username,
                                              password=args.password, protocol="ssh")
            l2vpn_obj = xe_native.Native()
            configure_l2vpn_xe(l2vpn_obj, remote_ip_address, intf_name, args.pw_id, args.pw_name)
        elif cisco_device["platform"] == "IOSXR":
            provider = NetconfServiceProvider(address=pe_ip_address, port=22, username=args.username,
                                              password=args.password, protocol="ssh")
            l2vpn_obj = l2vpn_xr_cfg.L2vpn()
            configure_l2vpn_xr(l2vpn_obj, remote_ip_address, intf_name, args.pw_id, args.pw_name)
        else:
            print("Invalid platform type entered!!")
            sys.exit()
        crud.create(provider, l2vpn_obj)
    

