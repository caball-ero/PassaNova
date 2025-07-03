import sqlite3 as sql
from flask import Flask, request, flash
from db import db_conn
from log import log
from string import ascii_lowercase, ascii_uppercase
from argon2 import PasswordHasher
from getpass import getpass
import logging
ph = PasswordHasher()


class User:
    def __init__(self, username, master_hash):
        self.username = username
        self.master_hash = master_hash

    # Creates the master password
    def setup_master(self, username, password):

        # Validates that the password is following the password policy
        if not pwd_policy(password):
            return {"status": False, "message": "Password does not meet the policy"}

        # Hashes the password after checking confirming that they match.
        try:
            hash = hasher(password)
            # Adds the password hash and the name to the database.
            with db_conn() as db:
                cr = db.cursor()
                cr.execute("INSERT INTO master (username , hash) VALUES (?,?)",
                           (username, hash))
                db.commit()
                return {"status": True}
        except Exception as e:
            return {"status": False, "message": str(e)}

    # Login functionality
    def login(self, username, password):

        # Checkes if the username and password exist and returns false if they don't
        stored_hash = master_exists(username)
        if not stored_hash:
            return False

        try:
            # If they exist it verifies the password and logs the user in if correct
            if ph.verify(stored_hash, password):
                return True

        except Exception as e:
            log(e)
            return False

        return False


# Hashing funciton using Argon2 hash
def hasher(master_pwd):
    hash = ph.hash(master_pwd)
    return hash


# Checks the database if the master exists
# Fetches the hash from the db by the name and returns it
def master_exists(name):
    try:
        with db_conn() as db:
            cr = db.cursor()
            cr.execute("SELECT hash FROM master where username = ? ", (name,))
            result = cr.fetchone()
            return result[0] if result else None
    except Exception as e:
        log(e)
        return None


# Validates the password
def pwd_policy(password):
    specials_chars = "!@#$%&*"
    lower = ascii_lowercase
    upper = ascii_uppercase

    if len(password) < 8:
        flash("Password is invalid\nPassword should not be less than 8 letters")
        return False

    if not any(c in specials_chars for c in password):
        flash("Password is invalid\nPassword should have at least one special character\n(! @ # $ % & *)")
        return False

    if not any(u in upper for u in password):
        flash("Password is invalid\nPassword should have at least 1 upper case letter")
        return False

    if not any(l in lower for l in password):
        flash("Password is invalid\nPassword should have at least 1 lower case letter")
        return False

    return True
