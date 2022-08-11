from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import logging
import os
import json

WORKING_DIR = os.getcwd()

def iterateThroughFiles():
    if(os.getcwd() == WORKING_DIR):
        os.chdir("./static/files")
    rootDir = os.getcwd()
    resultList = []
    
    for subdir, dirs, files in os.walk(rootDir):
        for file in files:
            resultList.append((os.path.join(subdir, file).replace(WORKING_DIR + "/static/files/", "")))
        for dir in dirs:
            resultList.append((os.path.join(subdir, dir).replace(WORKING_DIR + "/static/files/", "")))

    resultList.reverse()
    return resultList

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

#logging.basicConfig(
#        format='%(asctime)s %(levelname)-8s %(message)s',
#        level=logging.INFO,
#        datefmt='%Y-%m-%d %H:%M:%S',
#        filename='log.log')

app = Flask(__name__)
app.config["SECRET_KEY"] = "KOKOT"

app.config["UPLOAD_FOLDER"] = "static/files"

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

@app.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))
        return file.filename + " has been uploaded."
    return render_template("upload.html", form=form)    


@app.route("/files")
def files():
    return render_template("files.html", itemList=iterateThroughFiles())

if __name__ == "__main__":
    if(os.getenv("TESTING") == "True"):
        TESTING = True
    else:
        TESTING = False

    app.run(host="0.0.0.0", port=5000, debug=TESTING)