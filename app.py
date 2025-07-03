from flask import Flask, request, flash, redirect, session
from flask import render_template as render
from auth import *
from secrete import secret_key
from auth_routes import auth_bp
from vault_routes import vault_bp
from db import db_vault, init_db


app = Flask(__name__, template_folder='templates')
app.register_blueprint(auth_bp)
app.register_blueprint(vault_bp)
app.secret_key = secret_key
init_db()


@app.route('/')
def index():
    if not session.get("username"):
        return redirect("/login")
    return render('index.html')


@app.route("/vault")
def vault():
    if not session.get("username"):
        return redirect("/login")
    username = session.get("username")
    with db_vault() as db:
        cr = db.cursor()
        cr.execute(
            "SELECT site, id FROM vault WHERE username = ?", (username,))
        passowrds = [{"site": row[0], "id": row[1]} for row in cr.fetchall()]
    return render("vault.html", passwords=passowrds)


@app.route("/about")
def about():
    if not session.get("username"):
        return redirect("/login")
    return render("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
