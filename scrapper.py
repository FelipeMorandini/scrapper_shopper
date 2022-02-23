import json
import time
from playwright.sync_api import sync_playwright
import requests
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

config = dotenv_values("./.env")
base_url = "https://unica.shopper.com.br"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(no_viewport=True)
        page.goto(base_url, wait_until='load')
        
        print("Browser aberto na página.")
        
        # Fazendo login na plataforma
        # Por questões de segurança, utilizando variáveis de ambiente. Para testar, necessário setar seu próprio .env, com usuário e senha.
        
        page.click("#benefits div div:nth-child(1) span a")
        page.wait_for_timeout(2000)
        print('realizando login...')
        page.type("body div.login div div div div div.content div div div.slide div.access-login form div div:nth-child(2) input", config['USERNAME'])
        page.type("body div.login div div div div div.content div div div.slide div.access-login form div div:nth-child(3) input", config['PASSWORD'])
        page.click("body div.login div div div div div.content div div div.slide div.access-login form button")
        print('Tentativa de login em andamento...')
        page.wait_for_timeout(4000)
        
        # Checar se o login foi bem-sucedido
        
        try:
            page.wait_for_selector("div.sc-eZKLwX:nth-child(3) div:nth-child(1) button:nth-child(2)")
        except:
            print("O login não foi bem-sucedido. Por favor verifique se as credenciais foram inseridas corretamente.")
            exit()
        
        page.click("div.sc-eZKLwX:nth-child(3) div:nth-child(1) button:nth-child(2)")
        print('Login bem-sucedido. Redirecionando à página de compra única...')
        page.wait_for_timeout(4000)
        
        # ir para a aba de alimentos e início da coletaq das informações 
        
        page.goto(f"{base_url}/shop/alimentos/", wait_until='load')
        print("Redirecionando à página de alimentos...")
        page.wait_for_timeout(2000)
        
        subcategorias_element = page.query_selector_all("div.department div:nth-child(1) a:nth-child(2)")
        print("Capturando subcategorias")
        subcategorias = []
        for i in subcategorias_element:
            sub = i.get_attribute('href')
            subcategorias.append(sub)
        
        for i in subcategorias:
            page.goto(f"{base_url}{i}", wait_until='load')
            
            subcategoria = page.inner_text('.sc-hCwLRM')
            
            print(f"Capturando dados na subcategoria {subcategoria}")
            
            for j in range(100):
                page.mouse.wheel(0, 200)
            
            img = []
            nomes = []
            valores = []
            
            img_el = page.query_selector_all("div.sc-jcEtbA div:nth-child(1) div:nth-child(1) div:nth-child(1) div:nth-child(2) div:nth-child(1) img:nth-child(1)")
            nome_el = page.query_selector_all("div.sc-jcEtbA div:nth-child(1) div:nth-child(1) div:nth-child(1) div:nth-child(3) div:nth-child(1) p:nth-child(1)")
            valor_el = page.query_selector_all("div.sc-jcEtbA div:nth-child(1) div:nth-child(1) div:nth-child(1) div:nth-child(3) div:nth-child(2) div:nth-child(1) div:nth-child(1) p:nth-child(2)")
            
            for j in img_el:
                foto = j.get_attribute('src')
                img.append(foto)
            
            for j in nome_el:
                nome = j.inner_text()
                nomes.append(nome)
            
            for j in valor_el:
                valor = j.inner_text()
                valores.append(valor)
            
            for j in range(len(img_el)):
                print(f"Salvando produto {nomes[j]}")
                requests.post(
                    url='http://localhost:8000/products',
                    json = {
                        "name": nomes[j],
                        "price_to": float(valores[j].replace(',', '.')),
                        "image": img[j],
                        "department": "Alimentos",
                        "category": subcategoria,
                        "store": "Shopper",
                        "available": "S"
                    }
                )
        
        browser.close()

main()