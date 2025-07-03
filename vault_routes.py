from flask import Blueprint
from flask import Flask, request, flash, redirect, session
from flask import render_template as render
from auth import *
from vault import Vault
from cipher import Cipher
from forms import EditPasswordForm

vault_bp = Blueprint("vault_bp", __name__)

in_vault = Vault()
cipher = Cipher()


@vault_bp.route("/vault/add", methods=["GET", "POST"])
def add():
    if not session.get("username"):
        return redirect("/login")

    if request.method == "GET":
        return render("vault_add.html")
    try:
        password = request.form.get("password", "").strip()
        site = request.form.get("site", "").capitalize().strip()
        site_username = request.form.get("username", "").strip()
        username = session.get("username")
        master_password = request.form.get("masterkey", "").strip()

        if not all([password, site, site_username, master_password]):
            flash("All fields are required.")
            return render("vault_add.html")

        if not master_exists(username):
            flash("Incorrect Masterkey")
            return render("vault_add.html")

        result = cipher.encrypt(master_password, password.encode())
        if result is None:
            flash("Error occured while encrypting your password when saving it.")
            return render("vault_add.html")

        salt, nonce, ct = result
        in_vault.store(username=username, salt=salt, site=site,
                       site_username=site_username, nonce=nonce, ct=ct)
        flash("Password added successfully")
        return redirect("/vault")

    except Exception as e:
        log(e)
        flash("An error occured.")
        return render("vault_add.html")


@vault_bp.route("/vault/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    if not session.get("username"):
        return redirect("/login")
    try:
        if request.method == "POST":
            action = request.form.get("action")
            if action == "no":
                return redirect("/vault")
            if action == "yes":
                return redirect(f"/vault/delete/confirm/{id}")
    except Exception as e:
        flash("Something went wrong. Please try again")
        log(e)
    return render("delete.html", id=id)


@vault_bp.route("/vault/delete/confirm/<int:id>", methods=["GET", "POST"])
def delete_confirm(id):
    if not session.get("username"):
        return redirect("/login")
    try:
        if request.method == "POST":
            ph = PasswordHasher()
            password = request.form.get("masterkey")
            username = session.get("username")
            action = request.form.get("action")

            masterhash = master_exists(username)

            if action == "cancel":
                return redirect("/vault")

            if ph.verify(masterhash, password):
                with db_conn() as db:
                    cr = db.cursor()
                    cr.execute(
                        "DELETE FROM vault WHERE id = ? AND username = ?", (id, username))
                    db.commit()
                    flash("Password deleted successfully.")
                    return redirect("/vault")

            else:
                flash("Incorrect masterkey")
                return redirect(f"/vault/delete/confirm/{id}")
    except Exception as e:
        flash("something went wrong")
        log(e)
    return render("confirm.html", id=id)


@vault_bp.route("/vault/edit/confirm/<int:id>", methods=["GET", "POST"])
def edit_confirm(id):
    if not session.get("username"):
        return redirect("/login")
    try:
        if request.method == "POST":
            ph = PasswordHasher()
            password = request.form.get("masterkey")
            username = session.get("username")
            action = request.form.get("action")

            masterhash = master_exists(username)

            if action == "cancel":
                return redirect("/vault")

            if ph.verify(masterhash, password):
                return redirect(f"/vault/edit/{id}")
            else:
                flash("Masterkey is incorrect")
    except Exception as e:
        pass
    return render("edit_confirm.html", id=id)


@vault_bp.route("/vault/edit/<int:id>", methods=["GET", "POST"])
def edit_form(id):
    if not session.get("username"):
        return redirect("/login")

    username = session.get("username")
    form = EditPasswordForm()

    if request. method == "GET":
        with db_conn() as db:
            cr = db.cursor()
            cr.execute(
                "SELECT site, site_username FROM vault WHERE id = ? AND username = ?", (id, username))
            row = cr.fetchone()
            if row:
                form.site_username.data = row[1]
            else:
                flash("Entry not found")
                return redirect("/vault")

    if form.validate_on_submit():
        new_password = form.password.data.strip()
        site_username = form.site_username.data.strip()

        master_password = form.masterkey.data.strip()
        result = cipher.encrypt(master_password, new_password.encode())
        if result is None:
            flash("Error occured while encrypting your password.")
            return render("edit.html", id=id, form=form)

        salt, nonce, ct = result

        with db_conn() as db:
            cr = db.cursor()
            cr.execute("UPDATE vault SET site_username=?, salt=?, nonce=?, encryption=? WHERE id =? AND username=?",
                       (site_username, salt, nonce, ct, id, username))
            db.commit()
            flash("Password updated successfully.")
            return redirect("/vault")

    return render("edit.html", id=id, form=form)


@vault_bp.route("/vault/view_auth/<int:id>")
def view_auth(id):
    if not session.get("username"):
        return redirect("/login")

    username = session.get("username")

    if request.method == "POST":
        masterkey = request.form.get("masterkey")
        masterhash = master_exists(username)

        if ph.verify(masterhash, masterkey):
            return redirect(f"/vault/view/{id}")

    return render("view_auth.html")


@vault_bp.route("/vault/view/<int:id>")
def view(id):
    if not session.get("username"):
        return redirect("/login")
