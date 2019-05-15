import argparse
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_l2vpn_cfg as l2vpn_cfg
from ydk.types import Empty
import logging

log = logging.getLogger('ydk')
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
log.addHandler(handler)

def configure_l2vpn(l2vpn_instance, pe_ip_address, intf_name, pw_id, pw_name):
    '''Configure XConnect on PE device'''
    xconnectGroup = l2vpn_instance.Database.XconnectGroups.XconnectGroup()
    xconnectGroup.name = pw_name
    p2pXconnect = xconnectGroup.P2pXconnects.P2pXconnect()
    p2pXconnect.name = "p2p-ciscolive"
    pwid = p2pXconnect.Pseudowires.Pseudowire()
    pwid.pseudowire_id = int(pw_id)
    neighbor = pwid.Neighbor()
    neighbor.neighbor = pe_ip_address
    pwid_ac = p2pXconnect.AttachmentCircuits.AttachmentCircuit()
    pwid_ac.name = intf_name
    pwid.neighbor.append(neighbor)
    p2pXconnect.attachment_circuits.attachment_circuit.append(pwid_ac)
    p2pXconnect.pseudowires.pseudowire.append(pwid)
    xconnectGroup.p2p_xconnects.p2p_xconnect.append(p2pXconnect)
    l2vpn_instance.database.xconnect_groups.xconnect_group.append(xconnectGroup)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pe1_ip', nargs='?', help="IP address of PE1")
    parser.add_argument('--pe1_intf', nargs='?', help="Interface of PE1")
    parser.add_argument('--pe2_ip', nargs='?', help="IP address of PE2")
    parser.add_argument('--pe2_intf', nargs='?', help="Interface of PE2")
    parser.add_argument('--pw_id', nargs='?', help="Pseudo-wire ID")
    parser.add_argument('--pw_name', nargs='?', default="ciscolive", help="Pseudo-wire XConnect Name")
    parser.add_argument('--username', nargs='?', default="cisco", help="Username")
    parser.add_argument('--password', nargs='?', default="cisco", help="Password")
    args = parser.parse_args()
    cisco_devices = [{"ip_address":args.pe1_ip, "intf_name":args.pe1_intf, "dest_ip":args.pe2_ip},
            {"ip_address":args.pe2_ip, "intf_name":args.pe2_intf, "dest_ip":args.pe1_ip}]
    for cisco_device in cisco_devices:
        pe_ip_address = cisco_device["ip_address"]
        intf_name = cisco_device["intf_name"]
        dest_ip = cisco_device["dest_ip"]
        provider = NetconfServiceProvider(address=pe_ip_address, port=22, username=args.username, password=args.password, protocol="ssh")
        crud = CRUDService()
        
        l2vpn_instance = l2vpn_cfg.L2vpn()
        configure_l2vpn(l2vpn_instance, dest_ip, intf_name, args.pw_id, args.pw_name)
        crud.create(provider, l2vpn_instance)
    

