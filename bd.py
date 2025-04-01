import psycopg2
from dotenv import load_dotenv
import os
from cript import criptografar, descriptografar


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
        preference_almoco TEXT[] DEFAULT NULL,  
        preference_janta TEXT[] DEFAULT NULL     
    )
''')
    
    con.commit()
    con.close()
    

def inserir_usuario(username, password, preference, almoco, janta):
    con = connect()
    cursor = con.cursor()
    
    cursor.execute("SELECT 1 FROM contas WHERE username = %s", (username,))
    if cursor.fetchone():
        print(f"O usuário {username} já existe no banco de dados.")
    else:
        SS = criptografar(password)
        cursor.execute("INSERT INTO contas (username, password, preference, janta, almoco) VALUES (%s, %s, %s, %s, %s)", (username, SS, preference, almoco, janta))
        print(f"Usuário {username} inserido com sucesso.")
    
    con.commit()
    
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    cursor.close()
    con.close()
    print("Connection closed.")
    

def show_usuario():
    con = connect()
    cursor = con.cursor()
    
    cursor.execute("SELECT username, password, preference, janta, almoco FROM contas")
    contas = cursor.fetchall()
    
    con.commit()
    
    con.close()
    
    usuarios = []
    
    
    for usuario, senha_criptografada, preferencia, almoco, janta in contas:
        
        senha = descriptografar(senha_criptografada)  
        usuarios.append((usuario, senha, preferencia, almoco, janta))
    
    return usuarios



usuarios = show_usuario()
if usuarios:
    for usuario, senha, preferencia, almoco, janta in usuarios:  
        print(f"Usuário: {usuario}, Senha: {senha}, Preferência: {preferencia}, Almoco: {almoco}, Janta: {janta}")
else:
    print("Nenhum usuário encontrado.")

