from kafka import KafkaConsumer
import json

def print_bgp_neighbor(kafka_consumer, node, mdt_path):
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
                session_state = row["Content"]["session-state"]
            	print "neighbor {} is in {} state".format(neighbor_address, session_state)
            	
if __name__ == "__main__":
	consumer = KafkaConsumer('telemetry', bootstrap_servers=["198.18.134.32:9093"])
	node = "PE-1"
	mdt_path = "openconfig-bgp:bgp/neighbors/neighbor/state"
	
	print_bgp_neighbor(consumer, node, mdt_path)
