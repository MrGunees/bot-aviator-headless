import os
import time
from datetime import datetime
from estrategias import Estrategia15x, Estrategia10x
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TOKEN)

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

def enviar_telegram(msg):
    print(msg)
    try:
        bot.send_message(chat_id=CHAT_ID, text=msg)
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem para Telegram: {e}")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {msg}\n")

def capturar_vela():
    try:
        driver.get("https://br4.bet.br/play/3230")
        wait = WebDriverWait(driver, 15)
        elementos = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div.payout.ng-star-inserted')))
        if elementos:
            texto = elementos[-1].text.strip().replace("x", "").replace(",", ".")
            return float(texto)
    except Exception as e:
        print(f"❌ Erro ao capturar vela: {e}")
    return None

if __name__ == "__main__":
    estrategia1 = Estrategia15x()
    estrategia2 = Estrategia10x()
    historico = []

    while True:
        vela = capturar_vela()
        if vela:
            historico.append(vela)
            if len(historico) > 100:
                historico.pop(0)
            msg1 = estrategia1.analisar(historico)
            msg2 = estrategia2.analisar(historico)
            if msg1:
                enviar_telegram("Estratégia Gunees detectada: " + msg1)
            if msg2:
                enviar_telegram(msg2)
        else:
            print("📡 Buscando oportunidade...")
        time.sleep(60)
