import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# Konfiguration für InfluxDB
bucket = "population_vbg"
org = "example_org"
token = "your_token_here"
url = "http://localhost:8086"

# CSV-Datei laden
csv_file = "population.csv"
df = pd.read_csv(csv_file, delimiter="\t")

# Datumskonvertierung
df['stand'] = pd.to_datetime(df['stand'], format='%d.%m.%Y')

# InfluxDB-Client initialisieren
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Daten in InfluxDB schreiben
for index, row in df.iterrows():
    point = (
        Point("population")
        .tag("gemeinde", row['gemeinde'])
        .field("einwohner", int(row['einwohner']))
        .time(row['stand'], WritePrecision.NS)
    )
    write_api.write(bucket=bucket, org=org, record=point)

print("Daten erfolgreich in InfluxDB importiert.")
client.close()
