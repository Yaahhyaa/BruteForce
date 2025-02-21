import pandas as pd
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, WriteOptions
from datetime import datetime


bucket = "population_vbg"
org = "htld"
token = "6Er3r4RFQpBi7TNIwT2nM2LOHIzo5uvlxk7lIe0B5k47N6qzmOLPaHuxE1hkbmlGXAP0Dz2LWHlY_8VcPFw_Wg=="
url = "http://10.115.2.22:8086/"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))


csv_file = "data/ghd_kameralistik_vrv1997_ab_2006_bis_2019.csv"
df = pd.read_csv(csv_file, sep=";", engine="python")

df.columns = df.columns.str.strip()


required_columns = ["stand", "gemeinde", "einwohner"]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Die Spalte '{col}' fehlt in der Datei.")


df['stand'] = pd.to_datetime(df['stand'], format='%d.%m.%Y', errors='coerce')
df['einwohner'] = pd.to_numeric(df['einwohner'], errors='coerce')

df = df.dropna(subset=['stand', 'einwohner', 'gemeinde'])


for _, row in df.iterrows():
    point = (
        Point("population")
        .tag("location", row["gemeinde"])
        .field("einwohner", int(row["einwohner"]))
        .time(row["stand"], write_precision="s")
    )
    write_api.write(bucket=bucket, record=point)

print("Daten erfolgreich in InfluxDB importiert.")
write_api.close()
client.close()