import requests
import json
import time
from bs4 import BeautifulSoup

def send_offer(oferta):
    url = "http://localhost:3000/oferta"

    dados_oferta = {
        "title": oferta["title"],
        "price": oferta["price"],
        "image_url": oferta["image"]["url"],
        "source_url": oferta["sourceUrl"],
        "coupon_code": oferta.get("couponCode", "❌")
    }

    response = requests.post(url, json=dados_oferta)

    if response.status_code == 200:
        print("oferta enviada")
    else:
        print("Falha ao enviar a oferta. Código de status:", response.status_code)

def check_offers():
    url = "https://www.pelando.com.br/games-e-pc-gamer"

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        script_tag = soup.find("script", id="__NEXT_DATA__")

        if script_tag:
            json_content = json.loads(script_tag.contents[0])

            ofertas = json_content["props"]["pageProps"]["feedOffers"]["edges"]

            oferta_mais_recente = None
            timestamp_mais_recente = None

            for oferta in ofertas:
                timestamp_oferta = oferta["timestamps"]["createdAt"]
                if timestamp_mais_recente is None or timestamp_oferta > timestamp_mais_recente:
                    oferta_mais_recente = oferta
                    timestamp_mais_recente = timestamp_oferta

            if oferta_mais_recente:
                titulo = oferta_mais_recente["title"]
                preco = oferta_mais_recente["price"]
                url_imagem = oferta_mais_recente["image"]["url"]
                url_oferta = oferta_mais_recente["sourceUrl"]
                cupom_desconto = oferta_mais_recente["couponCode"] if "couponCode" in oferta_mais_recente and oferta_mais_recente["couponCode"] is not None else "❌"

                print("Nova oferta encontrada!")
                print("Título:", titulo)
                print("Preço:", preco)
                print("URL da Imagem:", url_imagem)
                print("URL da Oferta:", url_oferta)
                print("Cupom de Desconto:", cupom_desconto)

                send_offer(oferta_mais_recente)
            else:
                print("Nenhuma nova oferta encontrada.")
        else:
            print("Não foi possível encontrar o elemento com o JSON.")
    else:
        print("Falha ao fazer a requisição. Código de status:", response.status_code)

while True:
    check_offers()
    time.sleep(300)