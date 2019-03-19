from flask import Flask,render_template,request,session,url_for,redirect
from functions import json_response
from models.hospital import Hospital
from models.user import User
from decorators import login_required
import pusher

# 
import requests
from requests_toolbelt.adapters import appengine

app = Flask(__name__)
appengine.monkeypatch()
app.secret_key = "dgkj4urf989398011k2pjd"

# for admin website

pusher_client = pusher.Pusher(
  app_id='739264',
  key='f6f266841f565e4e7b21',
  secret='0d596bb7dafc11fdeaa5',
  cluster='ap1',
  ssl=True
)

@app.route("/",methods=["GET","POST"])
@app.route("/dashboard",methods=["GET","POST"])
@login_required
def index():
    pusher_client.trigger('hospital_channel', 'alert_event', 
            {'emergencyType': "Accident",
            'emergencyLocation' : "Mambaling Cebu City",
            'others': "3 people"
            })
    return render_template("index.html",title="Dashboard")

@app.route("/reports",methods=["GET","POST"])
@login_required
def reports():
    return render_template("reports.html",title="Reports")

@app.route("/responders",methods=["GET","POST"])
@login_required
def responders():
    return render_template("responders.html",title="Responders")

@app.route("/users",methods=["GET","POST"])
@login_required
def users():
    return render_template("users.html",title="Users")

@app.route("/settings",methods=["GET","POST"])
@login_required
def settings():
    return render_template("settings.html",title="Settings")

@app.route("/signin",methods=["GET","POST"])
def signin():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if "hospital_email" in data:
            hospital_email = data["hospital_email"]
        if "hospital_password" in data:
            hospital_password = data["hospital_password"]

        hospital = Hospital.signinHospital(hospital_email=hospital_email,hospital_password=hospital_password)
        if hospital:
            session['admin'] = hospital.key.id()
            return json_response({
                "signin": "success",
                "message" : "Sign in Success"
                })
        else:
            return json_response({
                "signin" : "failed",
                "message" : "Sign in failed"
                })
    return render_template("signin.html",title="Sign in")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if "hospital_name" in data:
            hospital_name = data["hospital_name"]
        if "hospital_address" in data:
            hospital_address = data["hospital_address"]
        if "hospital_email" in data:
            hospital_email = data["hospital_email"]
        if "hospital_contact" in data:
            hospital_contact = data["hospital_contact"]
        if "hospital_password" in data:
            hospital_password = data["hospital_password"]
        if "hospital_type" in data:
            hospital_type = data["hospital_type"]

        hospital = Hospital.addHospital(hospital_name=hospital_name,hospital_address=hospital_address,hospital_email=hospital_email,hospital_contact=hospital_contact,hospital_password=hospital_password,hospital_type=hospital_type)

        if hospital:
            return json_response({
                "signup" : "success",
                "message":"Successfully signed up"
                })
        else:
            return json_response({
                "signup" : "failed",
                "message":"Failed to sign up"
                })
            
    return render_template("signup.html",title="Sign up")

@app.route('/signout')
def signout():
    del session['admin']
    return redirect(url_for('signin'))

#for mobile user 

@app.route("/signup/user",methods=["GET","POST"])
def signup_user():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if "user_firstname" in data:
            user_firstname = data["user_firstname"]
        if "user_middlename" in data:
            user_middlename = data["user_middlename"]
        if "user_lastname" in data:
            user_lastname = data["user_lastname"]
        if "user_email" in data:
            user_email = data["user_email"]
        if "user_password" in data:
            user_password = data["user_password"]

        user = User.addUser(user_firstname=user_firstname,user_middlename=user_middlename,user_lastname=user_lastname,user_email=user_email,user_password=user_password)

        if user:
            return json_response({
                "signup" : "success",
                "message":"Successfully signed up"
                })
        else:
            return json_response({
                "signup" : "failed",
                "message":"Failed to sign up"
                })

@app.route("/signin/user",methods=["GET","POST"])
def signin_user():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if "user_email" in data:
            user_email = data["user_email"]
        if "user_password" in data:
            user_password = data["user_password"]

        user = User.signinUser(user_email=user_email,user_password=user_password)
        if user:
            return json_response({
                "signin": "success",
                "message" : "Sign in Success"
                })                  
        else:
            return json_response({
                "signin" : "failed",
                "message" : "Sign in failed"
                })

#for errors on admin website

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
