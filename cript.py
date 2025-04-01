from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
from dotenv import load_dotenv
import os

load_dotenv()

CHAVE_MESTRA = os.getenv("CHAVE_MESTRA").encode()

def key(salt: bytes):
    return PBKDF2(CHAVE_MESTRA, salt, dkLen=32)  # 256 bits

def criptografar(senha: str):
    salt = get_random_bytes(16)
    chave = key(salt)
    
    # Nonce de 8 bytes (64 bits) que é o padrão para AES-CTR
    nonce = get_random_bytes(8)
    cipher = AES.new(chave, AES.MODE_CTR, nonce=nonce)
    
    ciphertext = cipher.encrypt(senha.encode('utf-8'))
    
    # Armazena: salt (16) + nonce (8) + ciphertext
    encrypted_data = base64.b64encode(salt + nonce + ciphertext).decode('utf-8')
    return encrypted_data

def descriptografar(encrypted_data: str):
    encrypted_data = base64.b64decode(encrypted_data)
    
    salt = encrypted_data[:16]
    nonce = encrypted_data[16:24]  # 8 bytes
    ciphertext = encrypted_data[24:]
    
    chave = key(salt)
    cipher = AES.new(chave, AES.MODE_CTR, nonce=nonce)
    
    return cipher.decrypt(ciphertext).decode('utf-8')