import os
from log import log
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class Cipher:
    # Derives a key from the master password
    def derive_key(self, password: str, salt: bytes):
        """Derive a symmetric key from the password and salt."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=16,
            salt=salt,
            iterations=100_100,
            backend=default_backend()
        )
        return kdf.derive(password.encode())

    # Encrypts the passwords
    def encrypt(self, master_password: str, data: bytes):
        """Encrypt data with a key derived from the master password."""
        try:
            salt = os.urandom(16)
            key = self.derive_key(master_password, salt)
            aesgcm = AESGCM(key)
            nonce = os.urandom(12)
            ct = aesgcm.encrypt(nonce, data, None)
        except Exception as e:
            log(e)
            return None
        return salt, nonce, ct

    # Uses the salt derived from the master password and derives the key to dencrypt the password
    def decrypt(self, master_password: str, salt: bytes, nonce: bytes, ct: bytes):
        """Decrypt data with a key derived from the master password and salt."""
        try:
            key = self.derive_key(master_password, salt)
            aesgcm = AESGCM(key)
            data = aesgcm.decrypt(nonce, ct, None)
        except Exception as e:
            log(e)
            return None
        return data
