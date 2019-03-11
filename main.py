from flask import Flask,render_template,request
from functions import json_response
from models.hospital import Hospital

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
@app.route("/dashboard",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/reports",methods=["GET","POST"])
def reports():
    return render_template("reports.html")

@app.route("/responders",methods=["GET","POST"])
def responders():
    return render_template("responders.html")

@app.route("/users",methods=["GET","POST"])
def users():
    return render_template("users.html")

@app.route("/settings",methods=["GET","POST"])
def settings():
    return render_template("settings.html")
