
from ydk.services import ExecutorService
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_traceroute_act as xr_trace_act
from ydk.providers import NetconfServiceProvider
import logging

logger = logging.getLogger("ydk")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

provider = NetconfServiceProvider(address="198.18.1.11", port=22, username='cisco', password='cisco', protocol='ssh')
executor = ExecutorService()

trace = xr_trace_act.Traceroute()
trace.input.destination = trace.input.Destination()
trace.input.destination.destination = "192.168.0.2"

trace_output = executor.execute_rpc(provider, trace, trace.output)


