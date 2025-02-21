import random

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "S_FGx--eci6W9z2QICXNtr9tsgcl6qKVck76cnLJid3gr1lMUsk1K8uduW5hgAMme3G0SUq5KZcccagHACzK_w=="
org = "htld"
url = "http://10.115.2.22:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "monitoring"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

for value in range(100):
    rnd = random.randint(-50, 50)
    point = (
        Point("measurement1")
        .tag("tagname1", "tagvalue1")
        .field("field1", rnd)
    )
    write_api.write(bucket=bucket, org="htld", record=point)
    print(rnd)
    time.sleep(1)  # separate points by 1 second