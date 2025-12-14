import yfinance as yf
import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, MACD, ADXIndicator
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator

# ================= CONFIG =================
TICKER = "NVDA"
PERIOD = "1y"
# =========================================

# Descargar datos
df = yf.download(TICKER, period=PERIOD, auto_adjust=True)

# Comprobar si df está vacío
if df.empty:
    print(f"No se pudo descargar datos para {TICKER}. Verifica tu conexión a internet.")
    exit()

# Asegurarse de que la columna 'Close' sea Serie 1D
close = df["Close"].squeeze()
high = df["High"].squeeze()
low = df["Low"].squeeze()

# Precio actual
precio_actual = close.iloc[-1]

# Máximo histórico
ath = close.max()
dist_ath = ((precio_actual / ath) - 1) * 100

# ================= INDICADORES =================

# SMA
sma50 = SMAIndicator(close, 50).sma_indicator().iloc[-1]
sma200 = SMAIndicator(close, 200).sma_indicator().iloc[-1]

# MACD
macd = MACD(close)
macd_diff = macd.macd_diff().iloc[-1]
macd_signal = "ALCISTA" if macd_diff > 0 else "BAJISTA"

# ADX
adx = ADXIndicator(high, low, close).adx().iloc[-1]

# Bollinger Bands
bb = BollingerBands(close)
bb_sup = bb.bollinger_hband().iloc[-1]
bb_inf = bb.bollinger_lband().iloc[-1]

# RSI
rsi = RSIIndicator(close).rsi().iloc[-1]

# ================= ANÁLISIS =================

# Tendencia base
tendencia = "ALCISTA (Largo Plazo)" if sma50 > sma200 else "BAJISTA (Largo Plazo)"

# Fortaleza ADX
if adx < 20:
    fortaleza = "DÉBIL (Mercado lateral / Sin tendencia)"
elif adx < 30:
    fortaleza = "MODERADA"
else:
    fortaleza = "FUERTE"

# RSI Estado
if rsi < 30:
    estado_rsi = "SOBREVENTA (Posible rebote)"
elif rsi > 70:
    estado_rsi = "SOBRECOMPRA"
elif rsi < 45:
    estado_rsi = "VENDEDORA (Neutro-Débil)"
else:
    estado_rsi = "NEUTRA"

# Zona de precio
if precio_actual <= bb_inf:
    zona = "Zona de soporte (Barato)"
elif precio_actual >= bb_sup:
    zona = "Zona de resistencia (Caro)"
else:
    zona = "Zona neutral"

# Soportes / Resistencias simples
res_1m = high.tail(21).max()
sup_1m = low.tail(21).min()
res_3m = high.tail(63).max()
sup_3m = low.tail(63).min()

# ================= INFORME =================

print("=" * 55)
print(f"INFORME: {TICKER} (USD)")
print("=" * 55)
print(f"Precio actual:     {precio_actual:.2f} $")
print(f"Máximo histórico:  {ath:.2f} $")
print(f"Distancia al ATH:  {dist_ath:.2f} %")
print("-" * 55)

print("1. TENDENCIA & MOMENTUM:")
print(f"Tendencia base:    {tendencia}")
print(f"Señal MACD:       {macd_signal}")
print(f"Fortaleza (ADX):  {adx:.2f} → {fortaleza}")
print(f"SMA 50:           {sma50:.2f} $")
print(f"SMA 200:          {sma200:.2f} $")
print("-" * 55)

print("2. NIVELES DINÁMICOS (Bollinger):")
print(f"Resistencia BB:   {bb_sup:.2f} $")
print(f"Soporte BB:       {bb_inf:.2f} $")
print(f"Situación:        {zona}")
print("-" * 55)

print("3. NIVELES ESTÁTICOS:")
print("[CORTO PLAZO - 1 mes]")
print(f"Resistencia:      {res_1m:.2f} $")
print(f"Soporte:          {sup_1m:.2f} $")
print("[MEDIO PLAZO - 3 meses]")
print(f"Resistencia:      {res_3m:.2f} $")
print(f"Soporte:          {sup_3m:.2f} $")
print("-" * 55)

print("4. FUERZA (RSI):")
print(f"Valor RSI:        {rsi:.2f}")
print(f"Estado:           {estado_rsi}")
print("=" * 55)
