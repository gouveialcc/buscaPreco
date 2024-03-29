#    APLICACAO PARA REALIZAR PESQUISA DE PRECO E //
# DESCRICAO DE ITENS EM SITES UTILIZANDO O       //  
# METODO DE RASPAGEM DE WEB SITE (WEB SCRAPING)  //
# USANDO A BIBLIOTECA BEAUTIFULSOUP4.            //
# =================================================

# IMPORTAÇÃO DAS BIBLIOTECAS
# BIBLIOTECAS USADAS NO SCRAPING
from os import sep, times, write
from bs4.element import Tag
import requests
from bs4 import BeautifulSoup
import locale
# BIBLIOTECAS USADAS PARA ENVIO DE MENSAGEM WHATSAPP
import pywhatkit
import keyboard
import time
from datetime import datetime

# MÁSCARA MONETÁRIA
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# VARIÁVEIS GLOBAIS
url = 'https://www.mercadolivre.com.br/microsoft-xbox-one-s-1tb-standard-cor-branco/p/MLB14114827#reco_item_pos=1&reco_backend=machinalis-v2p-pdp-boost-v2&reco_backend_type=low_level&reco_client=vip-v2p&reco_id=6547dfe3-a60a-42a0-9c13-94f9b5a07f58'
prcDsj = 2.100

# FUNCAO REQUEST E SOUP DA URL
def request():
    global dscPrdt, valPrdt, valPrdtCnv
    site = requests.get(url)
    print(site.status_code, site.ok)

    # MONTANDO O SOUP
    soup = BeautifulSoup(site.content, 'html.parser')
    dscPrdt = soup.find('h1', class_='ui-pdp-title').get_text()
    valPrdt = soup.find('span', class_='price-tag-fraction').get_text()

    # CONVERTE O VALOR RETORNADO PARA VARIÁVEL EM FLOAT
    valPrdtCnv = float(valPrdt)
    print(f'>>> DESCRIÇÃO DO PRODUTO: {dscPrdt}.')
    print(f'>>> PREÇO: R${valPrdtCnv}.')

# FUNÇÃO ENVIA MENSAGEM WHATSAPP
def envMensagem():
    global contatos, x
    msgPrcAlcancado = (f"PREÇO ALCANÇADO PARA O PRODUTO: {dscPrdt}. AGORA ESTÁ NO VALOR DE R${valPrdtCnv}.")
    contatos = ['+5591991440764', '+5591991656408', '+5591980545716']
    x = 0

    while x <= 2:
        pywhatkit.sendwhatmsg(contatos[x], msgPrcAlcancado, datetime.now().hour, datetime.now().minute + 2, wait_time=10)
        time.sleep(30)
        keyboard.press_and_release('ctrl + w')
        x = x+1

# EXECUTA A FUNÇÃO DE PESQUISA WEB SCRAPING
request()

# CONDIÇÃO (PREÇO ALCANÇADO)
if(valPrdtCnv <= prcDsj):
    print(f'>>> PREÇO ALCANÇADO PARA O PRODUTO: {dscPrdt}, ESTÁ NO VALOR DE R${valPrdtCnv}.')
    envMensagem()
else:
    print(f'>>> PREÇO NÃO ALCANÇADO! O VALOR ATUAL É R${valPrdtCnv}.')

# REPETE O REQUEST ATÉ ALCANCAR O PREÇO DESEJADO
while valPrdtCnv > prcDsj:
    print(f'>>> PREÇO NÃO ALCANÇADO PARA O PRODUTO: {dscPrdt}.')
    print('>>> NOVO REQUEST SERÁ REALIZADO.')
    time.sleep(5)
    request()