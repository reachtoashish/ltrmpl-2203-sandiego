from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('telemetry', bootstrap_servers=["198.18.134.32:9093"])

for msg in consumer:
    telemetry_msg =  msg.value
    #print telemetry_msg
    telemetry_msg_json = json.loads(telemetry_msg)
    """
    if "Rows" in telemetry_msg_json:
        content_rows = telemetry_msg_json["Rows"]
        for row in content_rows:
            print row
            print "\n"
    """
    print json.dumps(telemetry_msg_json, sort_keys=True, indent=4)
