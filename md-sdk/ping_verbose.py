def process_ping_rpc(ping_output):
    """Process data in RPC output object."""
    # format string for reply header
    ping_reply_header = ('Sending 5, 100-byte ICMP Echos to {destination}, '
                         'timeout is 2 seconds:\n')
    # format string for reply trailer
    ping_reply_trailer = ('\nSuccess rate is {success_rate} percent '
                          '({hits}/{total}), '
                          'round-trip min/avg/max = {rtt_min}/{rtt_avg}/{rtt_max} ms')

    ping_response = ping_output.ping_response

    ping_reply = ping_reply_header.format(destination=ping_response.ipv4[0].destination)

    # iterate over all replies
    for reply in ping_response.ipv4[0].replies.reply:
        ping_reply += reply.result

    ping_reply += ping_reply_trailer.format(success_rate=ping_response.ipv4[0].success_rate,
                                            hits=ping_response.ipv4[0].hits,
                                            total=ping_response.ipv4[0].total,
                                            rtt_min=ping_response.ipv4[0].rtt_min,
                                            rtt_avg=ping_response.ipv4[0].rtt_avg,
                                            rtt_max=ping_response.ipv4[0].rtt_max,
                                            )

    # return formated string
    return ping_reply


from ydk.services import ExecutorService
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ping_act as xr_ping_act
from ydk.providers import NetconfServiceProvider
import logging

logger = logging.getLogger("ydk")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

provider = NetconfServiceProvider(address="198.18.1.11",
                                      port=22,
                                      username='cisco',
                                      password='cisco',
                                      protocol='ssh')
executor = ExecutorService()

ping = xr_ping_act.Ping()
ping.input.destination = ping.input.Destination()
ping.input.destination.destination = '192.168.0.2'
ping_output = executor.execute_rpc(provider, ping, ping.output)

print(process_ping_rpc(ping_output))

