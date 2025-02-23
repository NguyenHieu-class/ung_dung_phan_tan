import pandas as pd
from influxdb_client import InfluxDBClient
import warnings
from influxdb_client.client.warnings import MissingPivotFunction
warnings.simplefilter("ignore", MissingPivotFunction)

# Kết nối InfluxDB
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "nzo-PLTKMGQ2Z_NLIF-XX_UnmNQhimyAv8YkEkWSYjlLF1IXKmTVedq02CJYSfNqbo1qRt52w5Dbf35p8UR1_A=="
org = "thoi tiet"
bucket = "weatherv1"

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Truy vấn dữ liệu nhiệt độ
flux_query = f'''
from(bucket:"{bucket}")
  |> range(start: -8h)
  |> filter(fn: (r) => r["_measurement"] == "weather")
  |> filter(fn: (r) => r["_field"] == "temperature")
  |> keep(columns: ["_time", "_value"])
'''

df = query_api.query_data_frame(flux_query)

# Định dạng dữ liệu
df = df.rename(columns={'_time': 'time', '_value': 'temperature'})
df['time'] = pd.to_datetime(df['time'])
df = df.sort_values('time').reset_index(drop=True)

# Lưu dữ liệu ra file CSV
df.to_csv("../data/temperature_data.csv", index=False)

print("Dữ liệu đã được lưu vào data/temperature_data.csv")

client.close()
