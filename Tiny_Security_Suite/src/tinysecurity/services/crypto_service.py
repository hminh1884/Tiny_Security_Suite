import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class CryptoService:
    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=200_000
        )
        return kdf.derive(password.encode("utf-8"))

    @classmethod
    def encrypt_file(cls, source_path: str, target_path: str, password: str):
        with open(source_path, "rb") as f:
            data = f.read()
        salt = os.urandom(16)
        nonce = os.urandom(12)
        key = cls._derive_key(password, salt)
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, data, None)
        with open(target_path, "wb") as f:
            f.write(salt + nonce + ciphertext)

    @classmethod
    def decrypt_file(cls, source_path: str, target_path: str, password: str):
        with open(source_path, "rb") as f:
            file_data = f.read()
        salt = file_data[:16]
        nonce = file_data[16:28]
        ciphertext = file_data[28:]
        key = cls._derive_key(password, salt)
        aesgcm = AESGCM(key)
        decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
        with open(target_path, "wb") as f:
            f.write(decrypted_data)