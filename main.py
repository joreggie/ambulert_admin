from flask import Flask,render_template,request,session,url_for,redirect
from functions import json_response
from models.hospital import Hospital
from models.user import User
from models.responder import Responder
from models.report import Report
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
    return render_template("index.html",title="Dashboard")

@app.route("/reports",methods=["GET","POST"])
@login_required
def reports():
    return render_template("reports.html",title="Reports")

@app.route("/responders",methods=["GET","POST"])
@login_required
def responders():

    hospital = Hospital.get_by_id(int(session["admin"]))
    responders = Responder.query(Responder.hospital == hospital.key).order(-Responder.created).fetch()
    if responders != None:
        responder_dict = []
        for responder in  responders:
            responder_dict.append(responder.to_dict())
    else:
        responder_dict="Empty"

    if request.method == 'POST':
        data = request.get_json(force=True)
        if "responder_firstname" in data:
            responder_firstname = data["responder_firstname"]
        if "responder_middlename" in data:
            responder_middlename = data["responder_middlename"]
        if "responder_lastname" in data:
            responder_lastname = data["responder_lastname"]   
        hospital = Hospital.get_by_id(int(session["admin"]))
        responder = Responder.addResponder(hospital_id=hospital.key.id(),responder_firstname=responder_firstname,responder_middlename=responder_middlename,responder_lastname=responder_lastname)

        if responder:
            return json_response({
                "add" : "success",
                "message":"Successfully added responder"
                })
        else:
            return json_response({
                "add" : "failed",
                "message":"Failed to add responder"
                })  
    

    return render_template("responders.html",title="Responders",responders=responder_dict)

@app.route("/users",methods=["GET","POST"])
@login_required
def users():
    hospital = Hospital.get_by_id(int(session["admin"]))
    users = User.query(User.hospital == hospital.key).order(-User.created).fetch()
    if users != None:
        user_dict = []
        for user in users:
            user_dict.append(user.to_dict())
    else:
        user_dict="Empty"

    return render_template("users.html",title="Users",users=user_dict)

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

@app.route("/alert",methods=["POST"])
def alert():
    if request.method=='POST':
        data=request.get_json(force=True)
        if "location" in data:
            report_location =data["location"]
        if "emergencyType" in data:
            report_type =data["emergencyType"]
        if "others" in data:
            report_others =data["others"]

        report = Report.addReport(report_location=report_location,report_type=report_type,report_others=others)
        pusher_client.trigger("hospital_channel","alert_event",
            {
                "report_location": report_location,
                "report_type": report_type
            }
        )
        if report:
            return json_response({
                "add_report" : "success",
                "message":"Successfully sent report you can now await for hospitals to respond"
                })
        else:
            return json_response({
                "add_report" : "failed",
                "message":"Failed to send report"
                })

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
                "message" : "Sign in Success",
                "userid" : user.key.id(),
                "user_firstname" : user.user_firstname,
                "user_middlename" : user.user_middlename,
                "user_lastname" : user.user_lastname,
                "user_email" : user.user_email
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
