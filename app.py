from genericpath import exists
from operator import truediv
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, PasswordField
from werkzeug.utils import secure_filename
import os
import hashlib
import random
import string

ROOT_DIR = os.getcwd()
USERNAME = os.getenv("WEBSITE_USERNAME")
PASSWORD = os.getenv("WEBSITE_PASSWORD")
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

def iterateThroughFiles(username):
    os.chdir(ROOT_DIR)
    os.chdir("./files/" + username)
    userDir = os.getcwd()
    resultList = []
    
    for subdir, dirs, files in os.walk(userDir):
        for file in files:
            resultList.append((os.path.join(subdir, file).replace(ROOT_DIR + "/files/" + username + "/", "")))
        for dir in dirs:
            resultList.append((os.path.join(subdir, dir).replace(ROOT_DIR + "/files/" + username + "/", "")))

    resultList.reverse()
    return resultList

def generate_random_password(length):
	## shuffling the characters
	random.shuffle(characters)
	
	## picking random characters from the list
	password = []
	for i in range(length):
		password.append(random.choice(characters))

	## shuffling the resultant password
	random.shuffle(password)

	## converting the list to string
	## printing the list
	return "".join(password)

class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

#class LoginForm(FlaskForm):
    #username = StringField("Username", validators=[DataRequired()])

#logging.basicConfig(
#        format='%(asctime)s %(levelname)-8s %(message)s',
#        level=logging.INFO,
#        datefmt='%Y-%m-%d %H:%M:%S',
#        filename='log.log')

app = Flask(__name__)
app.config["SECRET_KEY"] = "KOKOT"
app.config["UPLOAD_FOLDER"] = "files"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    passwordHash = db.Column(db.String(256))
    salt = db.Column(db.String(32))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return render_template("index.html", page="index")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            return "user not found"

        password_hash = hashlib.sha256((password+user.salt).encode("utf-8")).hexdigest()
        if user.passwordHash == password_hash:
            login_user(user)
        else:
            return "incorrect password"
        return redirect(url_for("files"))
    

    return render_template("login.html", page="login")

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return "Logged out"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]

        if User.query.filter_by(username=username).first():
            return "User already exists"
        
        password = request.form["password"]
        salt = generate_random_password(32)
        password_hash = hashlib.sha256((password+salt).encode("utf-8")).hexdigest()
        user = User(username=username, passwordHash=password_hash, salt=salt)
        os.mkdir(ROOT_DIR + "/static/files/" + username)
        db.session.add(user)
        db.session.commit()
        logout_user()
        login_user(User.query.filter_by(username=username).first())
        return "Registered with username " + username
    

    return render_template("register.html")

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))
        return file.filename + " has been uploaded."
    return render_template("upload.html", form=form)    

@app.route("/download", methods=["GET"])
@login_required
def download():
    path = "./files/" + getattr(current_user, "username") + "/" + request.args["filename"]
    if exists(ROOT_DIR + "/files/" + getattr(current_user, "username") + "/" + request.args["filename"]):
        return send_file(path, as_attachment=True)
    else:
        return "File not found"

@app.route("/files")
@login_required
def files():
    print(getattr(current_user, "username"))
    return render_template("files.html", itemList=iterateThroughFiles(getattr(current_user, "username")), username=getattr(current_user, "username"))

if __name__ == "__main__":
    if(os.getenv("TESTING") == "True"):
        TESTING = True
    else:
        TESTING = False

    app.run(host="0.0.0.0", port=5000, debug=TESTING)