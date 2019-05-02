from flask import Flask,render_template,request,session,url_for,redirect
from functions import json_response
from models.hospital import Hospital
from models.user import User
from models.responder import Responder
from models.report import Report
from decorators import login_required
import pusher
import json
import logging

# 
import requests
from requests_toolbelt.adapters import appengine

app = Flask(__name__)
appengine.monkeypatch()
app.secret_key = "dgkj4urf989398011k2pjd"
app.config['FCM_APP_TOKEN'] = "AAAAVxwA4Zg:APA91bFz779TPyASpBPMa_gL94lRIC-yUaoTim8-bjC6nnFu4DkMoFAd9DljSj-nBQQE3b1UbHkdbxpRPpEzVEXC76el7Q-eDJ7k4K3KVum1pSfHRtuisuOO0Zi8DTCkZUO6ZQT2e0eu"

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
    hospital = Hospital.get_by_id(int(session["admin"]))

    accidents = Report.getAccidentsCount()
    pregnancy = Report.getPregnancyCount()
    illness = Report.getIllnessCount()

    recentReports = Report.getRecentReports()


    return render_template("index.html",title="Dashboard",hospital_name=hospital.hospital_name,accidents=accidents,pregnancy=pregnancy,illness=illness,recentReports=recentReports)

@app.route("/reports",methods=["GET","POST"])
@login_required
def reports():
    hospital = Hospital.get_by_id(int(session["admin"]))
    reports = Report.query().fetch()
    if reports != None:
        report_dict = []
        for report in  reports:
            report_dict.append(report.to_dict())
    else:
        report_dict="Empty"

    responders = Responder.query().fetch()
    if responders != None:
        responder_dict = []
        for responder in  responders:
            responder_dict.append(responder.dispatch())
    else:
        responder_dict="Empty"

    if request.method == "POST":
        data =  request.get_json(force=True)
        if 'report_id' in data:
            report_id = data['report_id']
        if 'report_option' in data:
            report_option = data['report_option']
        if 'responder' in data:
            responder = data['responder']
        
        report = Report.get_by_id(int(report_id))
        user_id = report.user
        user = User.get_by_id(int(user_id.id()))
        if report_option == "accepted":
            report_status = report_option
            Report.updateReport(report_id,report_status) #change report pending to accepter
            user_key = user.key.id()
            User.updateHospitalUser(user_key,hospital.key.id())
            Responder.assignRescue(responder_id=responder,report_info=report.key.id())
            pusher_client.trigger("accept_channel","accept_event",{"report_status": "accepted"})
            json_data = {
                "to" : user.fcm_token,
                "notification":{
                    "title" : "Hospital Response",
                    "body" : hospital.hospital_name + " has accepted your request for assistance"
                }
            }
            pusher_client.trigger("dispatch_channel","dispatch_event",
                {
                    "dispatch_status": "dispatched",
                    "hospital_name" : hospital.key.id(),
                    "message": hospital.hospital_name + " has accepted " + user.user_firstname +" "+ user.user_lastname + " request."
                }
            )
            
            logging.info(user.fcm_token)
            headers = {"content-type":"application/json","Authorization":"key=" + app.config["FCM_APP_TOKEN"]}
            requests.post("https://fcm.googleapis.com/fcm/send",headers=headers,data=json.dumps(json_data))
            
        elif report_option == "declined":
            report_status = report_option
            Report.updateReport(report_id,report_status)
            pusher_client.trigger("decline_channel","decline_event",
                {
                    "report_status": "declined",
                    "message": "You have declined " + user.user_firstname + "'s request for assistance"
                }
            )
            json_data = {
                "to" : user.fcm_token,
                "notification":{
                    "title" : "Hospital Response",
                    "body" : hospital.hospital_name + " has declined your request for assistance"
                }
            }
            headers = {"content-type":"application/json","Authorization":"key=" + app.config["FCM_APP_TOKEN"]}
            requests.post("https://fcm.googleapis.com/fcm/send",headers=headers,data=json.dumps(json_data))

        hospital = Hospital.get_by_id(int(session["admin"]))
    return render_template("reports.html",title="Reports",reports=report_dict,hospital_name=hospital.hospital_name,responders=responder_dict,hospital=session['admin'])

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
        if "responder_id" in data:
            responder_id = data["responder_id"]
        if "responder_firstname" in data:
            responder_firstname = data["responder_firstname"]
        if "responder_middlename" in data:
            responder_middlename = data["responder_middlename"]
        if "responder_lastname" in data:
            responder_lastname = data["responder_lastname"] 
        if "responder_option" in data:
            responder_option = data["responder_option"] 
        
        hospital = Hospital.get_by_id(int(session["admin"]))
        if responder_option == "add":
            responder = Responder.addResponder(hospital_id=hospital.key.id(),responder_firstname=responder_firstname,responder_middlename=responder_middlename,responder_lastname=responder_lastname,report_info="")

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
        elif responder_option == "edit":
            responder = Responder.updateResponder(responder_id=responder_id,responder_firstname=responder_firstname,responder_middlename=responder_middlename,responder_lastname=responder_lastname)

            if responder:
                return json_response({
                    "edit" : "success",
                    "message":"Successfully edited responder"
                    })
            else:
                return json_response({
                    "edit" : "failed",
                    "message":"Failed to edit responder"
                    }) 
        elif responder_option == "delete":
            responder=Responder.get_by_id(int(responder_id))
            responder.key.delete()

    return render_template("responders.html",title="Responders",responders=responder_dict,hospital_name=hospital.hospital_name)

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

    return render_template("users.html",title="Users",users=user_dict,hospital_name=hospital.hospital_name)

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

        hospital = Hospital.registeredHospital(hospital_name)
        
        #first trap
        if hospital is None:
            # if none result, register
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
        else:
            return json_response({
                "signup" : "duplicated",
                "message":"Entered duplicate hospital name"
                })
            
    return render_template("signup.html",title="Sign up")

@app.route('/signout')
def signout():
    del session['admin']
    return redirect(url_for('signin'))

#for mobile user 

@app.route("/user/reports",methods=["GET","POST"])
def user_reports():

    if request.method == "POST":
        data=request.get_json(force=True)
        if "userid" in data:
            userid = data["userid"] 
        user = User.get_by_id(int(userid))
        user_reports = Report.query(Report.user == user.key).order().fetch()
        if user_reports != None:
            report_dict = []
            for user_report in  user_reports:
                report_dict.append(user_report.to_dict())
            
            return json_response({
                "user_reports" : report_dict
            })
        else:
            return json_response({
                "user_reports" : "Empty"
            })

@app.route("/hospitals",methods=["GET"])
def hospitals():
    hospitals = Hospital.query().order(-Hospital.created).fetch()
    if hospitals != None:
        hospital_dict = []
        for hospital in  hospitals:
            hospital_dict.append(hospital.to_dict())
            
        return json_response({
            "hospitals" : hospital_dict
        })

@app.route("/responder/reports",methods=["GET","POST"])
def responder_report():
    if request.method == 'POST':
        data = request.get_json(force=True)
        if "responder_id" in data:
            responder_id = data["responder_id"]

        report_info = Responder.getReportInfo(responder_id)
        if report_info:
            return json_response({
                "report_info" : report_info
                })
        else:
            return json_response({
                "report_info" : "Empty"
                })


@app.route("/alert",methods=["POST"])
def alert():
    if request.method=='POST':
        data=request.get_json(force=True)
        if "userid" in data:
            user = data["userid"]
        if "location" in data:
            report_location =data["location"]
        if "emergencyType" in data:
            report_type =data["emergencyType"]
        if "others" in data:
            report_others =data["others"]
        if 'image' in data:
            report_image = data['image']
        
        report = Report.addReport(user_id=user,report_image=report_image,report_location=report_location,report_type=report_type,report_others=report_others,report_status="pending")
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

@app.route("/user-fcm",methods=["POST"])
def fcm_token():
    if request.method == "POST":
        data = request.get_json(force=True)
        if 'userid' in data:
            userid = data['userid']
        if 'token' in data:
            token = data['token']
        
        user = User.addToken(user_id=userid,token=token)

        if user:
            return json_response({
                "add_token" : "success",
                "message":"Successfully added token"
                })
        else:
            return json_response({
                "add_token" : "failed",
                "message":"Failed to add token"
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

        user = User.addUser(user_firstname=user_firstname,user_middlename=user_middlename,user_lastname=user_lastname,user_email=user_email,user_password=user_password,fcm_token="")

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

@app.route("/profile",methods=['POST'])
def profile():
    if request.method == "POST":
        data = request.get_json(force=True)
        if "user_id" in data:
            user_id = data["user_id"]
        if "user_firstname" in data:
            user_firstname = data["user_firstname"]
        if "user_middlename" in data:
            user_middlename = data["user_middlename"]
        if "user_lastname" in data:
            user_lastname = data["user_lastname"]
        if "user_email" in data:
            user_email = data["user_email"]

        user = User.updateProfile(user_id=user_id,user_firstname=user_firstname,user_middlename=user_middlename,user_lastname=user_lastname,user_email=user_email)

        if user:
            return json_response({
                "profile" : "updated",
                "message" : "Profile successfully updated."
            })
        else:
            return json_response({
                "profile" : "failed",
                "message" : "Failed to update profile."
            })


 #responder               
@app.route("/signin/responder",methods=["POST"])
def signin_responder():
    if request.method == 'POST':
        data = request.get_json(force=True)      

        if "responder_id" in data:
            responder_id = data["responder_id"]

        responder = Responder.get_by_id(int(responder_id))

        if responder:
            return json_response({
                "signin": "success",
                "message" : "Sign in Success",
                "responder_id" : responder.key.id(),
                "responder_firstname" : responder.responder_firstname,
                "responder_middlename" : responder.responder_middlename,
                "responder_lastname" : responder.responder_lastname,
                })                  
        else:
            return json_response({
                "signin" : "failed",
                "message" : "Sign in failed"
                })
@app.route("/responder/completion",methods=["POST"])
def responder_completion():

    if request.method == "POST":
        data=request.get_json(force=True)
        if "responder_id" in data:
            responderid = data["responder_id"] 

        responder = Responder.get_by_id(int(responder_id))
        if responder_id:
            responder.report_info == None
            responder.put()

        return json_response({
            "message" : "You have successfully completed the task." 
        })

#for errors on admin website

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404