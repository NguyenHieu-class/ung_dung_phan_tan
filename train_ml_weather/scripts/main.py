import pandas as pd
import numpy as np
import joblib
import time
import os
import pickle
from influxdb_client import InfluxDBClient
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

import warnings
from influxdb_client.client.warnings import MissingPivotFunction
warnings.simplefilter("ignore", MissingPivotFunction)

# ==== CẤU HÌNH KẾT NỐI INFLUXDB ====
INFLUXDB_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUXDB_TOKEN = "nzo-PLTKMGQ2Z_NLIF-XX_UnmNQhimyAv8YkEkWSYjlLF1IXKmTVedq02CJYSfNqbo1qRt52w5Dbf35p8UR1_A=="
INFLUXDB_ORG = "thoi tiet"
INFLUXDB_BUCKET = "weatherv1"

# ==== FETCH DATA ====
def fetch_temperature_data():
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: -3h)
        |> filter(fn: (r) => r["_measurement"] == "weather")
        |> filter(fn: (r) => r["_field"] == "temperature")
        |> keep(columns: ["_time", "_value"])
    '''
    query_api = client.query_api()
    result = query_api.query_data_frame(org=INFLUXDB_ORG, query=query)
    if isinstance(result, list) and len(result) > 0:
        df = result[0][["_time", "_value"]].rename(columns={"_time": "time", "_value": "temperature"})
        df.to_csv("../data/temperature_data.csv", index=False)
        print(f"Nhiệt độ hiện tại: {df['temperature'].iloc[-1]}°C")
        return df
    return None

# ==== TRAIN MODEL ====
def train_model():
    df = pd.read_csv("../data/temperature_data.csv")
    df["time"] = pd.to_datetime(df["time"]).astype(int) / 10**9
    X = df["time"].values.reshape(-1, 1)
    y = df["temperature"].values
    model = LinearRegression()
    model.fit(X, y)
    with open("../models/temp_trend_model.pkl", "wb") as f:
        pickle.dump(model, f)

# ==== PREDICT AND ALERT ====
def predict_and_alert():
    with open("../models/temp_trend_model.pkl", "rb") as f:
        model = pickle.load(f)
    df = pd.read_csv("../data/temperature_data.csv")
    df["time"] = pd.to_datetime(df["time"]).astype(int) / 10**9
    last_time = df["time"].iloc[-1]
    last_temp = df["temperature"].iloc[-1]
    future_time = np.array([[last_time + 3600]])
    predicted_temp = model.predict(future_time)[0]
    temp_change = predicted_temp - last_temp
    if temp_change >= 2:
        print("Cảnh báo: Nhiệt độ đang tăng mạnh!")
    elif temp_change >= 1:
        print("Cảnh báo: Nhiệt độ đang tăng nhẹ!")
    elif temp_change <= -2:
        print("Cảnh báo: Nhiệt độ đang giảm mạnh!")
    elif temp_change <= -1:
        print("Cảnh báo: Nhiệt độ đang giảm nhẹ!")

# ==== MAIN LOOP ====
if __name__ == "__main__":
    while True:
        df = fetch_temperature_data()
        if df is not None:
            train_model()
            predict_and_alert()
        time.sleep(60)
