import os

import psycopg2
from flask import Flask, flash, redirect, render_template, request


def get_connection():
    conn = psycopg2.connect(
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["HOST"],
        database=os.environ["DATABASE_NAME"],
        port=os.environ["DATABASE_PORT"],
    )
    return conn


app = Flask(__name__)
app.secret_key = "secret"


@app.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        query = "SELECT * FROM users WHERE name = %s AND password = %s"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name, password))
                user = cur.fetchone()
                if user:
                    return redirect("/mypage")
                else:
                    flash("Invalid username or password")
                    return redirect("/")
    else:
        return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        query = "INSERT INTO users (name, password) VALUES (%s, %s)"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (name, password))
                conn.commit()
        return redirect("/")
    else:
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
