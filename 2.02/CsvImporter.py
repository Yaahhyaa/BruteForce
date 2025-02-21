import influxdb_client
import pandas as pd
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Funktion für den InfluxDB-Client
def getInfluxClient():
    token = "6Er3r4RFQpBi7TNIwT2nM2LOHIzo5uvlxk7lIe0B5k47N6qzmOLPaHuxE1hkbmlGXAP0Dz2LWHlY_8VcPFw_Wg=="
    url = "http://10.115.2.22:8086/"
    org = "htld"
    influxClient = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    return influxClient

# Setze die Organisation und den Bucket
org = "htld"
bucket = "monitoring"

# Initialisiere den InfluxDB-Client
influxClient = getInfluxClient()
influxWriteAPI = influxClient.write_api(write_options=SYNCHRONOUS)

# Lese die CSV-Datei ein, achte auf das Dezimaltrennzeichen und das Semikolon als Trennzeichen
df = pd.read_csv('data/CovidFaelle_Timeline.csv', sep=';', encoding='utf-8', decimal=',')

# Konvertiere die Zeitspalte in ein datetime-Objekt (fehlerhafte Werte werden zu NaT)
df['Time'] = pd.to_datetime(df['# Time'], format='%d.%m.%Y %H:%M:%S', errors='coerce')

# Entferne alle Zeilen, bei denen das Datum ungültig ist
df = df.dropna(subset=['Time'])

# Iteriere über die Zeilen und schreibe die Daten in InfluxDB
for index, row in df.iterrows():
    point = (
        Point("CovidFaelle")
        .tag("Bundesland", row.get('Bundesland'))
        .tag("BundeslandID", str(row.get('BundeslandID')))
        .field("AnzahlFaelle", row.get('AnzahlFaelle'))
        .field("AnzahlTotSum", row.get('AnzahlTotSum'))
        .field("SiebenTageInzidenzFaelle", row.get('SiebenTageInzidenzFaelle'))
        .time(row['Time'])
    )
    influxWriteAPI.write(bucket=bucket, org=org, record=point)

# Schließe den Client nach dem Schreiben der Daten
influxClient.close()
