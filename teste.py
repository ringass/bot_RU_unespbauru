from Crypto.Random import get_random_bytes
import base64

chave = get_random_bytes(32)  # 32 bytes = 256 bits (tamanho ideal para AES)
print(base64.b64encode(chave).decode('utf-8'))