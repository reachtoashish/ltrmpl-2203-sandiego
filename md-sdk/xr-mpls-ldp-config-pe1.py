
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_mpls_ldp_cfg as xr_mpls_ldp_cfg
from ydk.types import Empty
import logging

"""
		Q:   What is the object/method/variable corresponding to the yang path variable?
		Ans: A python IDE will help autopopulate it. We have used jedi plugins for vim
"""


#The function gets the mpls_ldp object from the main function
#Also a list with interface names is passed on to this function from main
def config_ldp(mpls_ldp, ldp_interfaces):
    mpls_ldp.enable = Empty()          #as per the xml the </enable> variable doesnot have anything
    interface_list = mpls_ldp.default_vrf.interfaces.interface
                               #as per pyang/xml, above one is a list containing interface objects (which has name and enable inside)
    
    #in the below code for every interface to be configured, 
    #we are creating an instance of the ldp interface object
    #assigning the end variables i.e. interface_name to the actual interface string and enable varible to Empty.
    for intf in ldp_interfaces:
    	interface_obj = mpls_ldp.default_vrf.interfaces.Interface()
    
    	interface_obj.interface_name = intf
    	interface_obj.enable = Empty()
    	interface_list.append(interface_obj)

if __name__ == "__main__": 
    """Execute main program."""
   #create a netconf provider
    provider = NetconfServiceProvider(address="198.18.1.11", port=22, username="cisco", password="cisco", protocol="ssh")
    crud = CRUDService()
    
    ldp_interfaces = ["GigabitEthernet0/0/0/1", "GigabitEthernet0/0/0/2", "GigabitEthernet0/0/0/3"] 
    
    mpls_ldp = xr_mpls_ldp_cfg.MplsLdp() #create the instance of the MplsLDP object
    config_ldp(mpls_ldp, ldp_interfaces)  # invoke the function and pass on the mpls_ldp object and interface list

    crud.create(provider, mpls_ldp)   #validate and create netconf session to router validate and add the configuration
    exit()
