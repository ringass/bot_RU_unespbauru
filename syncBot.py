from playwright.sync_api import sync_playwright
from info.bd import show_usuario

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

def verifica_dinheiro(page):
    
    page.wait_for_selector('[href="/ru-bauru/dashboard/dashboard.do"]')
    page.click('[href="/ru-bauru/dashboard/dashboard.do"]')

    page.wait_for_selector(".card-subtitle")  
    preco_texto = page.locator(".card-subtitle").nth(1).text_content()
    preco_limpo = preco_texto.replace("R$", "").strip().replace(",", ".")
    preco = float(preco_limpo)
    
    if preco >= 25.00:
        print(f"Saldo suficiente para janta e almoço: R$ {preco:.2f}")
        return 2
    else:
        print(f"Saldo insuficiente para janta e almoço: R$ {preco:.2f}")

        if preco >= 12:
            print("Comprar apenas um periodo") 
            return 1
        else:
            print("Operacao cancelada")
            return 0
        
    
        
def acessar_RU(page):
    
    page.wait_for_selector('[href="https://sistemas.unesp.br/ru-bauru"]')
    page.click('[href="https://sistemas.unesp.br/ru-bauru"]')
    page.wait_for_timeout(5000)

    page.wait_for_selector('[href="/ru-bauru/cliente/selecionarFilaPorPeriodoDeAtendimento.do"]')
    page.click('[href="/ru-bauru/cliente/selecionarFilaPorPeriodoDeAtendimento.do"]')

    selecao = verifica_dinheiro(page)

    if selecao > 0:
        print("Pode continuar com a reserva da refeição.")
        # comprar_fila(page, selecao)
    else:
        print("Recarregar saldo antes de prosseguir.")
        
        
# def comprar_fila(page, int periodo):
    

    
def main(username: str, password: str, preferencia: str):
    
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()

        pagina(page)  
        login(page, username, password)  
        acessar_RU(page)
        
        print(page.title())  
        browser.close()


for usuario, senha, preferencia in show_usuario():
    main(usuario, senha, preferencia) #user, password, preference
