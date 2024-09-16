import os

import psycopg2
from flask import Flask, flash, redirect, render_template, request


def get_connection():
    return psycopg2.connect(
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["HOST"],
        database=os.environ["DATABASE_NAME"],
        port=os.environ["DATABASE_PORT"],
    )


app = Flask(__name__)
app.secret_key = "secret"


@app.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        name, password = request.form["name"], request.form["password"]
        with get_connection() as conn, conn.cursor() as cur:
            # cur.execute("SELECT * FROM users WHERE name = %s AND password = %s", (name, password))
            cur.execute(f"SELECT * FROM users WHERE name = '{name}' AND password = '{password}'")
            user = cur.fetchone()
            if user:
                return redirect("/mypage")
            else:
                flash("Invalid username or password", "flash-error")
        return redirect("/")
    else:
        return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name, password = request.form["name"], request.form["password"]
        with get_connection() as conn, conn.cursor() as cur:
            # cur.execute("INSERT INTO users (name, password) VALUES (%s, %s)", (name, password))
            cur.execute(f"INSERT INTO users (name, password) VALUES ('{name}', '{password}')")
            conn.commit()
        return redirect("/")
    return render_template("signup.html")


@app.route("/mypage", methods=["GET"])
def mypage():
    return render_template("mypage.html")


@app.route("/admin")
def admin():
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
    return render_template("admin.html", users=users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
