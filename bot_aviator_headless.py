import time
import json
from datetime import datetime
from estrategias import Estrategia15x, Estrategia10x
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram import Bot

TOKEN = '8141083778:AAGInpXEYV5LQYbpZocV7rDU4Lrk1NePDlA'
CHAT_ID = '1080444837'
bot = Bot(token=TOKEN)

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

def carregar_cookies():
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
    driver.get("https://br4.bet.br")
    time.sleep(3)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://br4.bet.br/play/3230")
    time.sleep(5)

def enviar_telegram(msg):
    print(msg)
    try:
        bot.send_message(chat_id=CHAT_ID, text=msg)
    except Exception as e:
        print(f"Erro Telegram: {e}")

def capturar_vela():
    try:
        elementos = driver.find_elements(By.CSS_SELECTOR, 'div.payout.ng-star-inserted')
        if elementos:
            texto = elementos[-1].text.strip().replace("x", "").replace(",", ".")
            return float(texto)
    except Exception as e:
        enviar_telegram(f"Erro ao capturar vela: {e}")
    return None

if __name__ == "__main__":
    estrategia1 = Estrategia15x()
    estrategia2 = Estrategia10x()
    historico = []

    enviar_telegram("✅ Bot Aviator iniciado com cookies (modo headless)")
    carregar_cookies()

    while True:
        vela = capturar_vela()
        if vela:
            historico.append(vela)
            if len(historico) > 100:
                historico.pop(0)
            msg1 = estrategia1.analisar(historico)
            msg2 = estrategia2.analisar(historico)
            if msg1: enviar_telegram(msg1)
            if msg2: enviar_telegram(msg2)
        else:
            enviar_telegram("⚠️ Vela não encontrada no ciclo.")
        time.sleep(60)