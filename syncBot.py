from playwright.sync_api import sync_playwright
from bd import show_usuario
import time
import requests
def pagina(page):
    
    page.goto("https://sistemas.unesp.br/")
    page.wait_for_selector(".link-central-de-acessos")
    page.click(".link-central-de-acessos")
    page.wait_for_timeout(5000)  

def login(page, username: str, password: str):
    
    page.wait_for_selector('[name="username"]')
    page.fill('[name="username"]', username)
    page.fill('[name="password"]', password)
    page.click('[name="button_entrar"]')
    page.wait_for_timeout(5000)

def verifica_dinheiro(page, almoco, janta):
    page.wait_for_selector('[href="/ru-bauru/dashboard/dashboard.do"]')
    page.click('[href="/ru-bauru/dashboard/dashboard.do"]')

    page.wait_for_selector(".card-subtitle")  
    preco_texto = page.locator(".card-subtitle").nth(1).text_content()
    preco_limpo = preco_texto.replace("R$", "").strip().replace(",", ".")
    preco = float(preco_limpo)

    
    preco_total = 2.50
    
    if preco >= preco_total:
        print(f"Saldo suficiente: R$ {preco:.2f} disponível")
        return True
    else:
        print(f"Saldo insuficiente: R$ {preco:.2f} disponível")
        return False
        

def acessar_RU(page, preferencia, almoco, janta):
    page.wait_for_selector('[href="https://sistemas.unesp.br/ru-bauru"]', timeout=10000)
    page.click('[href="https://sistemas.unesp.br/ru-bauru"]')
    
    
    # page.click('[href="/ru-bauru/dashboard/dashboard.do"]')

    
    if verifica_dinheiro(page, almoco, janta):
        print("Saldo suficiente para continuar.")
        
    page.wait_for_selector('[href="/ru-bauru/cliente/selecionarFilaPorPeriodoDeAtendimento.do"]', timeout=10000)
    page.click('[href="/ru-bauru/cliente/selecionarFilaPorPeriodoDeAtendimento.do"]')
    time.sleep(2)
    
    comprar_fila(page, preferencia, almoco, janta)     
    

def comprar_refeicao(page, periodo):
    
    period_map = {
        "almoco": 0,
        "janta": 1
    }
    
    periodo = periodo.lower()
    
    if periodo not in period_map:
        print(f"Período {periodo} inválido!")
        return

    period_index = period_map[periodo]
    
    period_selector = f"#form\\:j_idt26\\:{period_index}\\:j_idt27"
    
    page.wait_for_selector(period_selector, state="visible", timeout=30000)
    page.click(period_selector)
    
    page.wait_for_selector("#form\\:informacoes", state="visible", timeout=None)

def comprar_fila(page, periodo):
    periodo = periodo.lower()

    if periodo in ["almoco", "almoço"]:
        comprar_refeicao(page, "almoco")
        
        if janta:  
            comprar_refeicao(page, "janta")
    
    elif periodo in ["jantar", "janta"]:
        
        comprar_refeicao(page, "janta")
        
        if almoco:  
            comprar_refeicao(page, "almoco")  
        


def get_cf_cookies(url):
    response = requests.get(f"http://localhost:8000/cookies?url={url}")
    data = response.json()
    cookies = data.get("cookies", {})
    
    cf_cookies = []
    for name, value in cookies.items():
        cf_cookies.append({
            'name': name,
            'value': value,
            'domain': 'sistemas.unesp.br',
            'path': '/',
            'httpOnly': False,
            'secure': True,
            'sameSite': 'Lax'
        })
    return cf_cookies
        
  
def main(username: str, password: str, preferencia: str, almoco, janta):
    with sync_playwright() as p:
        
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        url = "https://sistemas.unesp.br/"
        cf_cookies = get_cf_cookies(url)
        context.add_cookies(cf_cookies)

        pagina(page)  
        login(page, username, password)  
        acessar_RU(page, preferencia, almoco, janta)
        
        print(page.title())  
        browser.close()


for usuario, senha, preferencia, almoco, janta in show_usuario():
    main(usuario, senha, preferencia, almoco, janta)
    
    