from cryptography.fernet import Fernet

from src.config.manager import settings

cipher = Fernet(settings.SECRET_KEY)


def encrypt_data(data: bytes) -> bytes:
    return cipher.encrypt(data)


def decrypt_data(encrypted_data: bytes) -> bytes:
    return cipher.decrypt(encrypted_data)
