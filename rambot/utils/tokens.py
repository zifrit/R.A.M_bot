import base64
import json
import time

import cryptography
from cryptography.fernet import Fernet

from config.settings import encryption_settings


# Генерация ключа
# def generate_key():
#     return Fernet.generate_key()


# Кодирование токена в строку
def encode_token_to_str(token):
    return base64.urlsafe_b64encode(token).decode()


# Декодирование токена из строки
def decode_token_from_str(token_str):
    return base64.urlsafe_b64decode(token_str.encode())


# Создание токена из JSON с меткой времени
def create_token(data, key):
    fernet = Fernet(key)
    data["timestamp"] = int(time.time())  # Добавляем текущую метку времени
    json_data = json.dumps(data)
    encrypted_data = fernet.encrypt(json_data.encode())
    return encode_token_to_str(encrypted_data)


# Расшифровка токена и проверка срока действия
def decrypt_token(token: str, key: bytes):
    try:
        token = decode_token_from_str(token)
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(token).decode()
    except Exception:
        return "Token invalid token"
    json_data = json.loads(decrypted_data)

    current_time = int(time.time())
    token_time = json_data.get("timestamp")

    if current_time - token_time > encryption_settings.TTL_ENCRYPTION_TOKEN:
        return "Token has expired"

    del json_data["timestamp"]  # Удаляем метку времени перед возвратом данных
    return json_data
