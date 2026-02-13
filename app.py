from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Izinkan akses dari frontend React

# ------------------------------
# 1. Endpoint Metrik Model
# ------------------------------
@app.route('/api/metrics')
def get_metrics():
    return jsonify({
        "mape": round(random.uniform(3.8, 5.2), 2),
        "rmse": round(random.uniform(1100, 1400), 2),
        "r2_score": round(random.uniform(0.89, 0.95), 4),
        "data_points": 48
    })

# ------------------------------
# 2. Endpoint Data Historis
# ------------------------------
@app.route('/api/historical')
def get_historical():
    data = []
    start_date = datetime(2021, 2, 1)
    price = 16200
    for i in range(60):  # 5 tahun = 60 bulan
        date = (start_date + timedelta(days=30 * i)).strftime('%Y-%m-%d')
        # Simulasi pergerakan harga
        price += random.randint(-200, 300)
        price = max(15000, min(35000, price))
        data.append({"date": date, "price": round(price)})
    return jsonify(data)

# ------------------------------
# 3. Endpoint Prediksi
# ------------------------------
@app.route('/api/predictions')
def get_predictions():
    data = []
    start_date = datetime(2026, 3, 1)
    price = 23400
    for i in range(12):  # 12 bulan ke depan
        date = (start_date + timedelta(days=30 * i)).strftime('%Y-%m-%d')
        price += random.randint(-100, 400)
        price = max(20000, min(30000, price))
        data.append({"date": date, "price": round(price)})
    return jsonify(data)

# ------------------------------
# 4. Endpoint Perubahan Harga (untuk chart volatilitas)
# ------------------------------
@app.route('/api/price-changes')
def get_price_changes():
    # Ambil data prediksi, lalu hitung perubahan
    preds = get_predictions().json
    changes = []
    for i, item in enumerate(preds):
        prev_price = 23400 if i == 0 else preds[i-1]["price"]
        change_usd = item["price"] - prev_price
        change_percent = (change_usd / prev_price) * 100
        changes.append({
            "month": item["date"],
            "previousPrice": prev_price,
            "currentPrice": item["price"],
            "changeUSD": change_usd,
            "changePercent": round(change_percent, 2)
        })
    return jsonify(changes)

# ------------------------------
# 5. Endpoint Komoditas Pembanding
# ------------------------------
@app.route('/api/commodities')
def get_commodities():
    data = []
    start_date = datetime(2025, 1, 1)
    nikel = 21000
    emas = 1950
    batubara = 140
    for i in range(14):  # Jan 2025 - Feb 2026
        date = (start_date + timedelta(days=30 * i)).strftime('%Y-%m-%d')
        nikel += random.randint(-300, 400)
        emas += random.randint(-20, 30)
        batubara += random.randint(-5, 8)
        data.append({
            "date": date,
            "nikel": round(nikel),
            "emas": round(emas),
            "batubara": round(batubara)
        })
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)