from flask import Blueprint
from flask import Flask, request, flash, redirect, session
from flask import render_template as render
from auth import *

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get("username"):
        return redirect("/")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if confirm != password:
            flash("Passwords do not match")
            return render("register.html")

        if master_exists(username):
            flash("Username already taken")
            return render("register.html")

        user = User(username, None)
        result = user.setup_master(username, password)
        if result["status"]:
            flash("Account created. Please log-in.")
            return redirect("/login")
        else:
            flash(result["message"])
    return render("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect("/")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username, None)
        if user.login(username, password):
            session["username"] = username
            return redirect('/')
        else:
            flash("Invalid Credentials")

    return render('login.html')


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    if not session.get("username"):
        return redirect("/")

    session.pop("username", None)  # Removes the username from session
    flash("You have been logged out.")
    return redirect("/login")
