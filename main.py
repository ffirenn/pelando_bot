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