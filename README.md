# pelando_bot

## Descrição
O `Pelando Bot` é um bot de scraping desenvolvido para extrair informações do site Pelando (https://www.pelando.com.br/). Ele é projetado para coletar dados sobre ofertas, cupons e promoções disponíveis na plataforma a cada 5 minutos e pode ser usado para diversos fins, como análise de preços, notificação de ofertas e muito mais.

## Funcionalidades
- Coleta dados de ofertas, cupons e promoções da Pelando.
- (AINDA NÃO FEITO) Envia as ofertas a um canal do Discord via Webhook.
- Armazena as ofertas recentes em um JSON para não haver envio de ofertas duplicadas.

## Breves funcionalidades
- Possibilidade de scrapar outras categorias da Pelando.
- Integração com o Discord para enviar as ofertas a um canal do Discord.
- Integração com o Telegram para enviar as ofertas a um canal do Telegram.

## Instalação

### Dependências Python
- Python 3.x
- Bibliotecas Python:
  - requests
  - BeautifulSoup

### Dependências Node.js
- Node.js 16.x
- Bibliotecas Node.js:
  - Discord.js 14.x
  - express

Você pode instalar as dependências Node.js usando o comando:
```bash
npm install
```
Você pode instalar as dependências Python usando o comando:
```bash
pip install -r requirements.txt
