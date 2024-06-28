# pip install pyTelegramBotAPI
# pip install python-dotenv
# pip install pyppeteer
from pyppeteer import launch
from dotenv import load_dotenv 
from bs4 import BeautifulSoup
import os
import asyncio

load_dotenv()
api_token = os.getenv("HTTP_API")
url = "https://es.aliexpress.com/item/1005005913185415.html?spm=a2g0o.home.0.0.376b70e5RxldFL&mp=1&gatewayAdapt=glo2esp"

# Tenemos que utilizar pyppeteer ya que parte de la página web se carga con javascript una vez la página ha sido cargada
async def get_html_page():
    navegador = await launch()
    pagina = await navegador.newPage()
    user_agent = "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"
    
    await pagina.setUserAgent(user_agent)
    await pagina.goto(url, {'waitUntil' : 'domcontentloaded'})
    await pagina.waitForSelector("div.product-price-current", visible=True)

    # Seleccionamos el switch del teclado que queremos
    boton_switches = await pagina.querySelector('div.sku-item--text--s0fbnzX:nth-child(1) > span:nth-child(1)')
    await boton_switches.click()
   
    # Obtener el contenido de la página
    pagina_html = await pagina.content()
    await navegador.close()
    return pagina_html           


# La función BeautifulSoup() nos permite extraer el código HTML
html = asyncio.get_event_loop().run_until_complete(get_html_page())
soup = BeautifulSoup(html, 'html.parser')
precio = soup.find('div', {'class' : 'product-price-current'})
hijos = precio.find_all(recursive=False)
precio_string = ''
for div in hijos:
    for span in div:
        precio_string = precio_string + str(span.text)

print(precio_string)