  
# from playwright.sync_api import sync_playwright
# from bd import show_usuario
# import time

# def pagina(page):
#     page.goto("https://sistemas.unesp.br/")
#     page.wait_for_selector(".link-central-de-acessos", timeout=10000)
#     page.click(".link-central-de-acessos")
#     time.sleep(2)

# def login(page, username: str, password: str):
#     page.wait_for_selector('[name="username"]', timeout=10000)
#     page.fill('[name="username"]', username)
#     page.fill('[name="password"]', password)
#     page.click('[name="button_entrar"]')
#     time.sleep(2)

# def verifica_saldo(page):
#     page.wait_for_selector('[href="/ru-bauru/dashboard/dashboard.do"]', timeout=10000)
#     page.click('[href="/ru-bauru/dashboard/dashboard.do"]')
    
#     page.wait_for_selector(".card-subtitle", timeout=10000)
#     saldo_texto = page.locator(".card-subtitle").nth(1).text_content()
#     saldo = float(saldo_texto.replace("R$", "").strip().replace(",", "."))
    
#     if saldo >= 25.00:
#         print(f"Saldo suficiente (R$ {saldo:.2f}) - Pode almoçar e jantar")
#         return 2
#     elif saldo >= 12.00:
#         print(f"Saldo moderado (R$ {saldo:.2f}) - Pode apenas um período")
#         return 1
#     else:
#         print(f"Saldo insuficiente (R$ {saldo:.2f}) - Operação cancelada")
#         return 0

# def comprar_refeicao(page, periodo: str):
#     periodo = periodo.lower()
#     if periodo in ["almoço", "almoco"]:
#         page.click("#form:j_idt26:0:j_idt27")
#     elif periodo in ["jantar", "janta"]:
#         page.click("#form:j_idt26:1:j_idt27")
#     time.sleep(2)

# def acessar_ru(page, preferencia: str):
#     page.wait_for_selector('[href="https://sistemas.unesp.br/ru-bauru"]', timeout=10000)
#     page.click('[href="https://sistemas.unesp.br/ru-bauru"]')
#     time.sleep(2)

#     page.wait_for_selector('[href="/ru-bauru/cliente/selecionarFilaPorPeriodoDeAtendimento.do"]', timeout=10000)
#     page.click('[href="/ru-bauru/cliente/selecionarFilaPorPeriodoDeAtendimento.do"]')
#     time.sleep(2)

#     saldo_status = verifica_saldo(page)
#     if saldo_status > 0:
#         comprar_refeicao(page, preferencia)
#     else:
#         print("Saldo insuficiente para realizar a compra")

# def executar_bot(username: str, password: str, preferencia: str):
#     with sync_playwright() as p:
#         browser = p.firefox.launch(headless=False)
#         page = browser.new_page()
        
#         try:
#             pagina(page)
#             login(page, username, password)
#             acessar_ru(page, preferencia)
#         except Exception as e:
#             print(f"Erro durante execução: {e}")
#         finally:
#             browser.close()

# if __name__ == "__main__":
#     usuarios = show_usuario()
#     if usuarios:
#         for usuario, senha, preferencia in usuarios:
#             print(f"Processando usuário: {usuario}")
#             executar_bot(usuario, senha, preferencia)
#     else:
#         print("Nenhum usuário encontrado no banco de dados")
        
        
        
        
        
        
        
        
from playwright.sync_api import sync_playwright
from bd import show_usuario
import time
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
        

def acessar_RU(page, preferencia):
    
    page.wait_for_selector('[href="https://sistemas.unesp.br/ru-bauru"]')
    page.click('[href="https://sistemas.unesp.br/ru-bauru"]')
    page.wait_for_timeout(5000)

    selecao = verifica_dinheiro(page)
    
    page.wait_for_selector('[href="/ru-bauru/cliente/selecionarFilaPorPeriodoDeAtendimento.do"]')
    page.click('[href="/ru-bauru/cliente/selecionarFilaPorPeriodoDeAtendimento.do"]')

    if selecao > 0:
        print("Pode continuar com a reserva da refeição.")
        comprar_fila(page, preferencia)     
    else:
        print("Recarregar saldo antes de prosseguir.")
        
        
def comprar_fila(page, periodo):
    periodo = periodo.lower()
    
    if periodo in ["almoço", "almoco"]:
        period_selector = "#form\\:j_idt26\\:0\\:j_idt27"
    elif periodo in ["jantar", "janta"]:
        period_selector = "#form\\:j_idt26\\:1\\:j_idt27"
    
    
    page.wait_for_selector(period_selector, state="visible", timeout=30000)
    page.click(period_selector)
    
    
    page.wait_for_selector("#form\\:informacoes", state="visible", timeout=None)

    
def main(username: str, password: str, preferencia: str):
    
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()

        pagina(page)  
        login(page, username, password)  
        acessar_RU(page, preferencia)
        
        print(page.title())  
        browser.close()


for usuario, senha, preferencia in show_usuario():
    main(usuario, senha, preferencia) #user, password, preference
    
    
    