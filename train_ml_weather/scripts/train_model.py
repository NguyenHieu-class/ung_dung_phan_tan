import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Đọc dữ liệu từ file CSV
df = pd.read_csv("../data/temperature_data.csv")
df['time'] = pd.to_datetime(df['time'])

# Tính toán đặc trưng
df['temp_diff'] = df['temperature'].diff()
df['temp_slope'] = df['temperature'].rolling(window=5).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0], raw=True)
df = df.dropna().reset_index(drop=True)

# Gán nhãn xu hướng
slope_threshold = 0.1
df['trend'] = df['temp_slope'].apply(lambda x: "increase" if x > slope_threshold else ("decrease" if x < -slope_threshold else "normal"))

# Chọn đặc trưng và nhãn
features = ['temp_diff', 'temp_slope']
X = df[features]
y = df['trend']

# Chia tập train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Đánh giá mô hình
y_pred = clf.predict(X_test)
print("\nBáo cáo đánh giá mô hình:")
print(classification_report(y_test, y_pred))

# Lưu mô hình
joblib.dump(clf, "../models/temp_trend_model.pkl")
print("\nMô hình đã được lưu vào models/temp_trend_model.pkl")
