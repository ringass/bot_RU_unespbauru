from playwright.sync_api import sync_playwright

def pagina(page):
    
    page.goto("https://sistemas.unesp.br/")
    page.wait_for_selector(".link-central-de-acessos")
    page.click(".link-central-de-acessos")
    page.wait_for_timeout(5000)  

def login(page, username: str, password: str):
    
    page.fill('[name="username"]', username)
    page.fill('[name="password"]', password)
    page.click('[name="button_entrar"]')
    page.wait_for_timeout(5000)

def RU(page):
    page.click('[href="https://sistemas.unesp.br/ru-bauru"]')
    page.wait_for_timeout(5000)

def main(username: str, password: str):
    
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        
        pagina(page)  
        login(page, username, password)  
        RU(page)
        
        print(page.title())  
        browser.close()


main("tomaz.gonzaga", "Gonzaga10") #CRIAR UM BD PARA ESCALAR!!