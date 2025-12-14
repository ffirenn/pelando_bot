<<<<<<< HEAD
import time
import hashlib
from datetime import datetime

from db import (
    init_db,
    get_offer,
    insert_offer,
    update_price,
    mark_sent
)
from scraper import fetch_latest_offers
from sender import send_offer

limit = 3
CHECK_INTERVAL = 5

init_db()
print("bot iniciado. monitorando ofertas...")

while True:

    offers = fetch_latest_offers(limit=limit)

    if not offers:
        print("nenhuma oferta encontrada")
        time.sleep(CHECK_INTERVAL)
        continue

    offer = offers[0]
    print(f"oferta encontrada: {offer['title']} | R$ {offer['price']}")

    offer_id = hashlib.md5(
        offer["sourceUrl"].encode()
    ).hexdigest()

    db_offer = get_offer(offer_id)
    should_send = False

    if not db_offer:
        print("oferta nova, salvando no banco")
        insert_offer(offer_id, offer)
        should_send = True
    else:
        _, _, _, _, current_price, last_sent_price, *_ = db_offer

        if offer["price"] != current_price:
            print(f"preço mudou: {current_price} → {offer['price']}")
            update_price(offer_id, offer["price"])

        if last_sent_price is None or offer["price"] < last_sent_price:
            print("preço menor que o último enviado")
            should_send = True
        else:
            print("oferta já enviada anteriormente")

    if should_send:
        payload = {
            "title": offer["title"],
            "price": offer["price"],
            "image_url": offer.get("image", {}).get("url"),
            "source_url": offer["sourceUrl"],
            "coupon_code": offer.get("couponCode") or "❌"
        }

        print("enviando oferta...")

        if send_offer(payload):
            mark_sent(offer_id, offer["price"])
            print("oferta enviada com sucesso")
        else:
            print("falha ao enviar oferta")

    time.sleep(CHECK_INTERVAL)
=======
import os
import json
import requests
import time
from bs4 import BeautifulSoup

DATA_FILE = "last_offer_data.json"

last_offer_data = {"title": "", "price": ""}

def load_last_offer_data():
    global last_offer_data

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            last_offer_data = json.load(file)

def save_last_offer_data():
    global last_offer_data

    with open(DATA_FILE, "w") as file:
        json.dump(last_offer_data, file)

def send_offer(offer):
    global last_offer_data

    url = "http://localhost:3000/oferta"

    offer_data = {
        "title": offer["title"],
        "price": offer["price"],
        "image_url": offer["image"]["url"],
        "source_url": offer["sourceUrl"],
        "coupon_code": offer.get("couponCode", "❌")
    }

    if offer_data["title"] != last_offer_data["title"] or offer_data["price"] != last_offer_data["price"]:
        response = requests.post(url, json=offer_data)

        if response.status_code == 200:
            print("Oferta enviada")
            last_offer_data["title"] = offer_data["title"]
            last_offer_data["price"] = offer_data["price"]
            save_last_offer_data()
        else:
            print("Falha ao enviar a oferta. Código de status:", response.status_code)
    else:
        print("A oferta é a mesma que a última oferta enviada. Não será enviada novamente.")

def check_offers():
    url = "https://www.pelando.com.br/games-e-pc-gamer"

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        script_tag = soup.find("script", id="__NEXT_DATA__")

        if script_tag:
            json_content = json.loads(script_tag.contents[0])

            offers = json_content["props"]["pageProps"]["feedOffers"]["edges"]

            latest_offer = None
            latest_timestamp = None

            for offer in offers:
                offer_timestamp = offer["timestamps"]["createdAt"]
                if latest_timestamp is None or offer_timestamp > latest_timestamp:
                    latest_offer = offer
                    latest_timestamp = offer_timestamp

            if latest_offer:
                title = latest_offer["title"]
                price = latest_offer["price"]
                image_url = latest_offer["image"]["url"]
                source_url = latest_offer["sourceUrl"]
                coupon_code = latest_offer["couponCode"] if "couponCode" in latest_offer and latest_offer["couponCode"] is not None else "❌"

                print("Nova oferta encontrada!")
                print("Título:", title)
                print("Preço:", price)
                print("URL da Imagem:", image_url)
                print("URL da Oferta:", source_url)
                print("Cupom de Desconto:", coupon_code)

                send_offer(latest_offer)
            else:
                print("Nenhuma nova oferta encontrada.")
        else:
            print("Não foi possível encontrar o elemento com o JSON.")
    else:
        print("Falha ao fazer a requisição. Código de status:", response.status_code)

load_last_offer_data()

while True:
    check_offers()
    time.sleep(300)
>>>>>>> a0e7edc80b76e198a806a46f45130b35879ce94a
