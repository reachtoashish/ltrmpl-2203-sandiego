import argparse
import sys
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_l2vpn_cfg \
    as l2vpn_cfg
from ydk.types import Empty
import logging


def configure_l2vpn():
    xconnectGroup = l2vpn_instance.Database.XconnectGroups.XconnectGroup()
    xconnectGroup.name = "ciscolive"
    p2pXconnect = xconnectGroup.P2pXconnects.P2pXconnect()
    p2pXconnect.name = "p2p-ciscolive"
    pwid = p2pXconnect.Pseudowires.Pseudowire()
    pwid.pseudowire_id = 201
    neighbor = pwid.Neighbor()
    neighbor.neighbor = "192.168.0.2"
    pwid_ac = p2pXconnect.AttachmentCircuits.AttachmentCircuit()
    pwid_ac.name = "GigabitEthernet0/0/0/0.200"
    pwid_ac.enable = Empty()

    pwid.neighbor.append(neighbor)
    p2pXconnect.attachment_circuits.attachment_circuit.append(pwid_ac)
    p2pXconnect.pseudowires.pseudowire.append(pwid)
    xconnectGroup.p2p_xconnects.p2p_xconnect.append(p2pXconnect)
    l2vpn_instance.database.xconnect_groups.xconnect_group.append(xconnectGroup)

if __name__ == "__main__":
    provider = NetconfServiceProvider(address="198.18.1.11", port=22, username="cisco", password="cisco", protocol="ssh")
    crud = CRUDService()

    l2vpn_instance = l2vpn_cfg.L2vpn()
    configure_l2vpn()

    crud.create(provider, l2vpn_instance)

    sys.exit()


