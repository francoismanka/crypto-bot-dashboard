
from binance.client import Client
from decimal import Decimal
import time
import numpy as np
import os
import requests
from dotenv import load_dotenv

# Charger les clés API depuis .env
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Configuration
SYMBOL = "BTCUSDT"
CAPITAL_INITIAL = Decimal("100.0")
QUANTITE = Decimal("10.0")
TAKE_PROFIT = Decimal("0.2")
STOP_LOSS = Decimal("0.2")
INTERVAL = 60  # Vérification chaque minute

# Variables
capital = CAPITAL_INITIAL
prix_achat = None
historique = []

# Connexion Binance
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

# URL du serveur en ligne (à remplacer par l'URL Render après déploiement)
SERVER_URL = "https://TON_URL_RENDER/log"

def get_price():
    ticker = client.get_symbol_ticker(symbol=SYMBOL)
    return Decimal(ticker['price'])

def rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    deltas = np.diff(prices)
    gains = deltas[deltas > 0].sum() / period
    losses = -deltas[deltas < 0].sum() / period
    rs = gains / losses if losses != 0 else 0
    return 100 - (100 / (1 + rs))

def macd(prices, short=12, long=26, signal=9):
    if len(prices) < long:
        return None, None
    short_ema = np.mean(prices[-short:])
    long_ema = np.mean(prices[-long:])
    macd_line = short_ema - long_ema
    signal_line = np.mean(prices[-signal:])
    return macd_line, signal_line

def send_log(price, rsi_val, macd_val, capital, message):
    data = {
        "price": str(price),
        "rsi": str(rsi_val),
        "macd": str(macd_val),
        "capital": str(capital),
        "message": message
    }
    try:
        requests.post(SERVER_URL, json=data)
    except:
        print("Impossible d'envoyer les données au tableau de bord.")

# BOT
print("--- BOT PRO AVEC DASHBOARD EN LIGNE ---")
while True:
    try:
        prix_actuel = get_price()
        historique.append(float(prix_actuel))
        if len(historique) > 50:
            historique.pop(0)

        current_rsi = rsi(np.array(historique))
        macd_line, signal_line = macd(np.array(historique))
        message = f"Prix actuel : {prix_actuel}"

        if prix_achat is None and current_rsi and macd_line:
            if current_rsi < 40 and macd_line > signal_line:
                prix_achat = prix_actuel
                message = f">> Achat virtuel à {prix_actuel} USDT"

        elif prix_achat:
            variation = ((prix_actuel - prix_achat) / prix_achat) * 100
            if variation >= TAKE_PROFIT:
                gain = QUANTITE * (variation / 100)
                capital += gain
                message = f">> Vente (TP)! Gain : {gain:.2f} USDT | Capital : {capital:.2f} USDT"
                prix_achat = None
            elif variation <= -STOP_LOSS:
                perte = QUANTITE * (abs(variation) / 100)
                capital -= perte
                message = f">> Vente (SL)! Perte : {perte:.2f} USDT | Capital : {capital:.2f} USDT"
                prix_achat = None

        send_log(prix_actuel, current_rsi, macd_line, capital, message)
        print(message)
        time.sleep(INTERVAL)

    except Exception as e:
        print(f"Erreur : {e}")
        time.sleep(10)
