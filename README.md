# PassaNova

**Secure, modern password manager built with Python & Flask.**

> PassaNova stores your credentials in an AES‑256‑GCM–encrypted vault, protected by an Argon2‑hashed master password. 100% local encryption, zero plaintext exposure.

---

## Features

- **Argon2‑protected master account** — strong, salted hashing
- **Full CRUD vault** — create, read, update, delete credentials
- **AES‑256‑GCM encryption** — per‑entry nonce & PBKDF2‑derived key
- **Re‑authentication gates** — sensitive operations prompt for password again
- **Modular OOP design** — separate `Cipher` (crypto) & `Vault` (data) classes
- **Flask Web UI** — clean, responsive templates
- **Logging & error handling** — secure logging without leaking secrets

---

## Architecture at a Glance

```
          +------------+
          |  Browser   |
          +-----+------+                +-------------+
                | HTTP(S) requests      |  Database   |
+---------------v---------------+       |  (SQLite)   |
|            Flask              |       +------+------+
|  ┌──────────────┐   ┌────────┐ |
|  |  Routes    |   | Render  | |
|  |  /login    |   |  HTML   | |
|  └─────────┘   └───────┘ |
|        | session auth         |       +------+------+
|  +-----v-----+       +--------v---+   +------+------+
|  |  Cipher   |<----->|   Vault    |<--|  Cipher     |
|  +-----------+       +------------+   +-------------+
|      (AES‑GCM)         (CRUD ops)         (Argon2)   |
+------------------------------------------------------+
```

---

## Tech Stack

| Layer    | Tech                                    |
| -------- | --------------------------------------- |
| Language | Python 3.12                             |
| Web      | Flask, Jinja2                           |
| Crypto   | `cryptography` (AES‑GCM), `argon2‑cffi` |
| DB (dev) | SQLite (MySQL planned)                  |
| Frontend | HTML5, CSS (Bootstrap‑lite)             |

---

## Quickstart

```bash
# 1. Clone repo
$ git clone https://github.com/<your‑user>/PassaNova.git
$ cd PassaNova

# 2. Create & activate virtual env
$ python -m venv venv
$ source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
$ pip install -r requirements.txt

# 4. Set a FLASK_SECRET_KEY env var or edit config.py

# 5. Run
$ python run.py
```

Open `http://127.0.0.1:5000` in your browser and create your master account.

---

## Security Notes

1. **Master Password** ➔ Argon2id (time_cost = 3, memory_cost = 64 MB, parallelism = 4)
2. **Vault Entries** ➔ AES‑256‑GCM with per‑entry 12‑byte nonce
3. **Key Derivation** ➔ PBKDF2‑HMAC‑SHA256, 100k iterations, unique 16‑byte salt per entry
4. **No credentials in logs** — errors are logged securely via `logging.exception()`.

---

## Roadmap

- Search & filtering interface
- 2‑Factor Authentication (TOTP)
- Migrate to MySQL for production
- Encrypted export / import
- Automated test suite (pytest)

---

## Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

1. Fork the repo & clone locally.
2. Create a feature branch: `git checkout -b feature/awesome`.
3. Commit & push: `git push origin feature/awesome`.
4. Open a PR.

---

## License

This project is licensed under the **MIT License** — see `LICENSE` for details.
