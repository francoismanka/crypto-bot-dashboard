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
TAKE_PROFIT = Decimal("0.2")  # +0.2%
STOP_LOSS = Decimal("0.2")    # -0.2%
INTERVAL = 60  # Vérification chaque minute

# Variables
capital = CAPITAL_INITIAL
prix_achat = None

# Connexion Binance (données réelles en testnet)
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'

# Récupérer le prix actuel
def get_price():
    ticker = client.get_symbol_ticker(symbol=SYMBOL)
    return Decimal(ticker['price'])

print(f"--- SIMULATION BOT ---\nCrypto : {SYMBOL} | Capital initial : {capital} USDT\n")

while True:
    try:
        prix_actuel = get_price()
        print(f"Prix actuel {SYMBOL} : {prix_actuel} USDT")

        if prix_achat is None:
            prix_achat = prix_actuel
            print(f">> Achat virtuel à {prix_achat} USDT")
        else:
            variation = ((prix_actuel - prix_achat) / prix_achat) * 100
            print(f"Variation : {variation:.3f}%")

            if variation >= TAKE_PROFIT:
                gain = QUANTITE * (variation / 100)
                capital += gain
                print(f">> Vente (TP) ! Gain : {gain:.2f} USDT | Capital : {capital:.2f} USDT")
                prix_achat = None

            elif variation <= -STOP_LOSS:
                perte = QUANTITE * (abs(variation) / 100)
                capital -= perte
                print(f">> Vente (SL) ! Perte : {perte:.2f} USDT | Capital : {capital:.2f} USDT")
                prix_achat = None

        time.sleep(INTERVAL)

    except Exception as e:
        print("Erreur :", e)
        time.sleep(10)
