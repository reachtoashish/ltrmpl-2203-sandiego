import os
from kafka import KafkaConsumer
import json
from time import ctime

def bgp_neighbor_established(kafka_consumer, node, mdt_path, neighbor_ip):
    # iterate over all arriving messages
    for kafka_msg in kafka_consumer:
        msg = json.loads(kafka_msg.value.decode('utf-8'))
        # if message is operational BGP data
        if (msg["Telemetry"]["node_id_str"] == node and
                msg["Telemetry"]["encoding_path"] == mdt_path
                and "Rows" in msg):
            for row in msg["Rows"]:
                # if neighbor in intended session state
                neighbor_address = row["Keys"]["neighbor-address"]
                if (neighbor_address == neighbor_ip):
                	session_state = row["Content"]["session-state"]
            		print "{} : neighbor {} is in {} state".format(ctime(), neighbor_address, session_state)
            		if (session_state == "ESTABLISHED"):
            			return True
            			
            		
if __name__ == "__main__":
	consumer = KafkaConsumer('telemetry', bootstrap_servers=["198.18.134.32:9093"])
	node = "PE-1"
	RR1_ip = "192.168.0.100"
	RR2_ip = "192.168.0.200"
	mdt_path = "openconfig-bgp:bgp/neighbors/neighbor/state"
	RR1_script = "python3 ../md-sdk+telemetry/configure_bgp_neighbor.py 1 192.168.0.100 1 ssh://cisco:cisco@198.18.1.11:22"
	RR2_script = "python3 ../md-sdk+telemetry/configure_bgp_neighbor.py 1 192.168.0.200 1 ssh://cisco:cisco@198.18.1.11:22"
	
	print "{} : Provisioning RR1 peer".format(ctime())
	if not os.system(RR1_script):
		print "{} : Provisioned RR1 peer".format(ctime())
		print "{} : Tracking RR1 peer state through MDT(Model Driven Telemetry)".format(ctime())
		if bgp_neighbor_established(consumer, node, mdt_path, RR1_ip):
			print "{} : RR1 neighbor state changed to Established. provisioning RR2 peer".format(ctime())
			if not os.system(RR2_script):
				print "{} : Provisioned RR2 peer".format(ctime())
				print "{} : Tracking RR2 peer state through MDT(Model Driven Telemetry)".format(ctime())
				if bgp_neighbor_established(consumer, node, mdt_path, RR2_ip):
					print "{} : RR2 neighbor state changed to Established. Exiting script".format(ctime())
