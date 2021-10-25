#    APLICACAO PARA REALIZAR PESQUISA DE PRECO E //
# DESCRICAO DE ITENS EM SITES UTILIZANDO O       //  
# METODO DE RASPAGEM DE WEB SITE (WEB SCRAPING)  //
# USANDO A BIBLIOTECA BEAUTIFULSOUP4.            //
# =================================================

# IMPORTACAO DAS BIBLIOTECAS
# BIBLIOTECAS USADAS NO SCRAPING
from os import sep, times, write
from bs4.element import Tag
import requests
from bs4 import BeautifulSoup
# BIBLIOTECAS USADAS PARA ENVIO DE MENSAGM WHATSAPP
import pywhatkit
import keyboard
import time
from datetime import datetime
import locale

# MASCARA MONETARIA
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# VARIÁVEIS GLOBAIS
url = 'https://www.mercadolivre.com.br/microsoft-xbox-one-s-1tb-standard-cor-branco/p/MLB14114827#reco_item_pos=1&reco_backend=machinalis-v2p-pdp-boost-v2&reco_backend_type=low_level&reco_client=vip-v2p&reco_id=6547dfe3-a60a-42a0-9c13-94f9b5a07f58'
prcDsj = 2.900
prcDsjCnv = str(prcDsj)

# FUNCAO REQUEST E SOUP SITE MERCADO LIVRE
def request():
    global v1ml, v2ml, v2ml_value
    siteml = requests.get(url)
    print(siteml.status_code, siteml.ok)

    # MONTANDO O SOUP ML
    soupml = BeautifulSoup(siteml.content, 'html.parser')
    v1ml = soupml.find('h1', class_='ui-pdp-title').get_text()
    v2ml = soupml.find('span', class_='price-tag-fraction').get_text()

    # CONVERTE O VALOR RETORNADO DA VARIÁVEL DO PRECO ACIMA
    v2ml_value = float(v2ml)
    print(f'>>> DESCRIÇÃO DO PRODUTO: {v1ml}')
    print(f'>>> PREÇO: R${v2ml_value}')

# FUNCAO ENVIA MENSAGEM WHATSAPP
def envMensagem():
    global contatos, x
    msgPrcAlcancado = (f"PREÇO ALCANÇADO PARA O PRODUTO {v1ml}, ESTÁ NO VALOR DE R${v2ml_value}")
    contatos = ['+5591991440764', '+5591991656408', '+5591980545716']
    x = 0

    while x <= 2:
        pywhatkit.sendwhatmsg(contatos[x], msgPrcAlcancado, datetime.now().hour, datetime.now().minute + 2)
        time.sleep(60)
        keyboard.press_and_release('ctrl + w')
        x = x+1

# EXECUTA A FUNCAO DE PESQUISA WEB SCRAPING
request()

# CONDICAO (PREÇO ALCANÇADO)
if(prcDsj <= v2ml_value):
    print(f'>>> PREÇO ALCANÇADO PARA O PRODUTO: {v1ml}, ESTÁ NO VALOR DE R${v2ml_value}.')
    envMensagem()
else:
    print(f'>>> PREÇO NÃO ALCANÇADO! O VALOR ATUAL É R${v2ml_value}.')

# REPETE O REQUEST ATÉ ALCANCAR O PRECO DESEJADO
while prcDsj > v2ml_value:
    time.sleep(5)
    request()