
from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Stockage des logs en mémoire
logs = []

@app.route('/log', methods=['POST'])
def receive_log():
    data = request.get_json()
    if data:
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        entry = {
            "time": timestamp,
            "price": data.get("price"),
            "rsi": data.get("rsi"),
            "macd": data.get("macd"),
            "capital": data.get("capital"),
            "message": data.get("message")
        }
        logs.append(entry)
        return jsonify({"status": "Log received"}), 200
    return jsonify({"error": "Invalid data"}), 400

@app.route('/')
def dashboard():
    return render_template('dashboard.html', logs=logs[-20:])  # Derniers 20 logs

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
