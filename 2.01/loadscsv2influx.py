import pandas as pd

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "S_FGx--eci6W9z2QICXNtr9tsgcl6qKVck76cnLJid3gr1lMUsk1K8uduW5hgAMme3G0SUq5KZcccagHACzK_w=="
org = "htld"
url = "http://10.115.2.22:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket = "monitoring"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

# Read data from CSV
df = pd.read_csv('data/cli_mem.csv', sep=",", header=0)
print(df)

# Write data to InfluxDB
for index, row in df.iterrows():
    point = (
        Point("mem")
        .tag("host", row['host'])
        .field("used_percent", row['used_percent'])
        .time(row['time'])  # Assuming the 'time' column is in the correct format
    )

    print(point.to_line_protocol())
    write_api.write(bucket=bucket, org=org, record=point)