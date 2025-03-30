import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()


USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

def connect():
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    
    print("Connection successful!")
    
    return connection

def create_table():
    con = connect()
    cursor = con.cursor()
      
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contas (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        preference TEXT NOT NULL
    )
    ''')
    
    con.commit()
    con.close()
    

def inserir_usuario(username, password, preference):
    con = connect()
    cursor = con.cursor()
    
    cursor.execute("SELECT 1 FROM contas WHERE username = %s", (username,))
    if cursor.fetchone():
        print(f"O usuário {username} já existe no banco de dados.")
    else:
        cursor.execute("INSERT INTO contas (username, password, preference) VALUES (%s, %s, %s)", (username, password, preference))
        print(f"Usuário {username} inserido com sucesso.")
    
    con.commit()
    
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    cursor.close()
    con.close()
    print("Connection closed.")
    

inserir_usuario("user", "senha", "preferencia") #coneção com front para receber de algum lugar e inserir

def show_usuario():
    con = connect()
    cursor = con.cursor()
    
    cursor.execute("SELECT username, password, preference FROM contas")
    contas = cursor.fetchall()
    
    con.commit()
    
    con.close()
    return contas

usuarios = show_usuario()
if usuarios:
    for usuario, senha, preferencia in usuarios:
        print(f"Usuário: {usuario}, Senha: {senha}, Preferência: {preferencia}")
else:
    print("Nenhum usuário encontrado.")
