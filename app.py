from flask import Flask, render_template, request
import logging

#logging.basicConfig(
#        format='%(asctime)s %(levelname)-8s %(message)s',
#        level=logging.INFO,
#        datefmt='%Y-%m-%d %H:%M:%S',
#        filename='log.log')

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", page="index")

@app.route("/login/")
def login():
    return render_template("login.html", page="login")

@app.route("/register")
def register():
    return render_template("register.html", page="register")

@app.route("/login_resolve", methods=["POST"])
def login_resolve():
    if request.method == "POST":
        data = request.form
        for x in data:
            print(data["username"])
            print(data["password"])
        return "thx"

@app.route("/register_resolve", methods=["POST"])
def register_resolve():
    if request.method == "POST":
        data = request.form
        sql = "INSERT INTO credentials (username, passwordHash) VALUES (%s, %s);"
        val = (data["username"], data["password"])
        return "ty, registered"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)