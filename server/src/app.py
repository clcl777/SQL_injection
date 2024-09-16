import os

from flask import Flask, flash, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app: Flask) -> None:
    db.init_app(app)


def set_config(app: Flask) -> None:
    app.config.update(
        SECRET_KEY="dev",
        WTF_CSRF_SECRET_KEY="csrf",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}".format(
            **{
                "user": os.environ["POSTGRES_USER"],
                "password": os.environ["POSTGRES_PASSWORD"],
                "host": os.environ["HOST"],
                "database_name": os.environ["DATABASE_NAME"],
                "port": os.environ["DATABASE_PORT"],
            }
        ),
    )


app = Flask(__name__)
set_config(app)
init_db(app)
app.secret_key = "secret"


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


@app.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        name, password = request.form["name"], request.form["password"]
        user = User.query.filter_by(name=name, password=password).first()
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
        user = User(name=name, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("signup.html")


@app.route("/mypage", methods=["GET"])
def mypage():
    return render_template("mypage.html")


@app.route("/admin")
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=80, debug=True)
