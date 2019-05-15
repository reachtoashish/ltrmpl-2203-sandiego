import argparse
import sys
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xe import Cisco_IOS_XE_native as xe_native
from ydk.types import Empty
from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
import logging

log = logging.getLogger('ydk')
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
log.addHandler(handler)

def configure_xe_l2vpn():
    intf = xe_l2vpn.Interface.GigabitEthernet()
    intf.name = "5.201"
    intf_encap = intf.Encapsulation()
    intf_encap_dot1q = intf_encap.Dot1Q()
    intf_encap_dot1q.vlan_id = 201
    xe_xconnect = intf.Xconnect()
    xe_xconnect.address = "192.168.0.1"
    xe_xconnect.vcid = 201
    xe_xconnect_encap = xe_xconnect.Encapsulation()
    xe_xconnect.encapsulation = xe_xconnect_encap.mpls
    intf.xconnect = xe_xconnect
    intf_encap.dot1q = intf_encap_dot1q
    intf.encapsulation = intf_encap
    xe_l2vpn.interface.gigabitethernet.append(intf)

if __name__ == "__main__":
    provider = NetconfServiceProvider(address="198.18.1.12", port=830, username="cisco", password="cisco", protocol="ssh")
    crud = CRUDService()
    #provider = CodecServiceProvider(type='xml')
    #codec = CodecService()
    xe_l2vpn = xe_native.Native()
    configure_xe_l2vpn()
    crud.create(provider, xe_l2vpn)
    #print(codec.encode(provider, xe_l2vpn))
    sys.exit()
