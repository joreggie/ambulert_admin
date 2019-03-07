from flask import Flask,render_template,request
from functions import json_response
from models.hospital import Hospital

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    if request.method=="POST":
        data = request.get_json(force=True)
        
        hospital = Hospital.addHospital(
            hospital_name=data["hospital_name"],
            hospital_address=data["hospital_address"],
            hospital_contact=data["hospital_contact"],
            hospital_type=data["hospital_type"])

        if hospital:
            return json_response({
                "message" : "Successfuully signed up!"  
            })
        else:
            return json_response({
                "message" : "Sign up failed!"
            })

    return render_template("index.html")
