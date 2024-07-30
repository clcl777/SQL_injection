import os

import psycopg2
from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DATABASE_URI = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}".format(
    **{
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
        "host": os.environ["HOST"],
        "database_name": os.environ["DATABASE_NAME"],
        "port": os.environ["DATABASE_PORT"],
    }
)


def get_connection():
    conn = psycopg2.connect(
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["HOST"],
        database=os.environ["DATABASE_NAME"],
        port=os.environ["DATABASE_PORT"],
    )
    return conn


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


app = Flask(__name__)
app.config.update(SQLALCHEMY_TRACK_MODIFICATIONS=False, SQLALCHEMY_DATABASE_URI=DATABASE_URI, SECRET_KEY="key")
db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        query = f"SELECT * FROM users WHERE name = '{name}' AND password = '{password}'"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
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
        query = f"INSERT INTO users (name, password) VALUES ('{name}', '{password}')"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
        return redirect("/")
    else:
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
