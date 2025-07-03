from db import db_vault, db_conn
import base64
from log import log
from cipher import Cipher


class Vault:
    def __init__(self):
        self.cipher = Cipher()

    # Stores the data in the database
    def store(self, username, site_username, site, salt,  ct, nonce):
        """Store encrypted data and parameters in the database."""
        salt_b64 = base64.b64encode(salt).decode('utf-8')
        ct_b64 = base64.b64encode(ct).decode('utf-8')
        nonce_b64 = base64.b64encode(nonce).decode('utf-8')
        try:
            with db_vault() as db:
                cr = db.cursor()
                cr.execute("INSERT INTO vault (username, site_username, site, salt, encryption, nonce) VALUES (?, ?, ?, ?, ?, ?)",
                           (username, site_username, site, salt_b64, ct_b64, nonce_b64))
                db.commit()
        except Exception as e:
            log(e)
            return None

    # Retrieves the password from the database and decrypt it.
    def retrieve_decrypt(self, site, masterkey):
        try:
            with db_vault() as db:
                cr = db.cursor
                try:
                    cr.execute(
                        "SELECT salt, nonce, encryption FROM vault WHERE site = ?", (site,))
                    row = cr.fetchone()
                except Exception as e:
                    log(e)
                    return None
        except Exception as e:
            log(e)
            return None

        if not row:
            return None
        salt_b64, nonce_b64, ct_b64 = row
        salt = base64.b64decode(salt_b64)
        nonce = base64.b64decode(nonce_b64)
        ct = base64.b64decode(ct_b64)

        decrypted_password = self.cipher.decrypt(masterkey, salt, nonce, ct)

        return decrypted_password
