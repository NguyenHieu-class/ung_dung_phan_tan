import pandas as pd
import numpy as np
import joblib

# Load mô hình
clf = joblib.load("../models/temp_trend_model.pkl")

# Đọc dữ liệu gần đây nhất từ file CSV
df = pd.read_csv("../data/temperature_data.csv")
df['time'] = pd.to_datetime(df['time'])

# Hàm tính độ dốc của xu hướng nhiệt độ
def compute_slope(x):
    if len(x) < 2:
        return 0
    t = np.arange(len(x))
    slope = np.polyfit(t, x, 1)[0]
    return slope

# Hàm kiểm tra và cảnh báo nhiệt độ
def check_and_alert(new_temperature):
    # Lấy dữ liệu gần đây nhất
    recent_temps = df['temperature'].tail(4).tolist()
    recent_temps.append(new_temperature)

    # Tính đặc trưng mới
    new_temp_diff = new_temperature - df['temperature'].iloc[-1]
    new_temp_slope = compute_slope(recent_temps)

    # Dự đoán xu hướng
    X_new = np.array([[new_temp_diff, new_temp_slope]])
    prediction = clf.predict(X_new)[0]

    # Hiển thị cảnh báo
    print(f"\n🔥 Nhiệt độ hiện tại: {new_temperature}°C")
    print(f"📉 Độ chênh lệch nhiệt độ: {new_temp_diff:.2f}")
    print(f"📈 Độ dốc xu hướng: {new_temp_slope:.2f}")

    if prediction == "increase":
        print("🚨 CẢNH BÁO: Nhiệt độ đang tăng mạnh!")
    elif prediction == "decrease":
        print("❄️ CẢNH BÁO: Nhiệt độ đang giảm mạnh!")
    else:
        print("✅ Nhiệt độ ổn định.")

# Kiểm tra với giá trị giả lập
check_and_alert(21)  # Thay bằng nhiệt độ thực tế
