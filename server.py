from flask import Flask, render_template, jsonify
import os
from decimal import Decimal
import time

app = Flask(__name__, template_folder='.')

# Variables globales du bot
capital = Decimal("100.00")
last_action = "Aucune action"
last_update = time.strftime("%Y-%m-%d %H:%M:%S")

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/data')
def data():
    return jsonify({
        "capital": str(capital),
        "last_action": last_action,
        "last_update": last_update
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
