from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://localhost:5432/login-demo"
app.secret_key = "I like vegatables!"


db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(
        db.String(100),
        primary_key = True
    )
    
    password = db.Column(
        db.String(100)
    )

@app.route('/')
def home():
    username = session.get('username') or "Noboby"
    return render_template("home.html", username = username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # do the login
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username = username).first()
        success = False
        if user and user.password == password:
            success = True
        
        if success:
            session['username'] = username
            return redirect('/')
        return render_template("login.html", success = success, username = username)
    else:
        return render_template("login.html")
        
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        message = None
        # 1. passwords match
        if password != confirm_password:
            message = "Passwords do not match"
        else:
            # 2. username does not already exist in DB
            user = User.query.filter_by(username = username).first()
            if user:
                message = "User already exists"
            else:
                # 3. Add user to DB
                user = User(username = username, password = password)
                db.session.add(user)
                db.session.commit()
                session["username"] = username
                return redirect('/')
        
        return render_template("signup.html", message = message)
    else:
        return render_template("signup.html")
    