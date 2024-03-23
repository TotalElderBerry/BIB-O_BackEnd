from flask import render_template,redirect,url_for,request
from models.login import login_event_organizer

def login():

    if request.method == "POST":
        if login_event_organizer(): 
            return redirect(url_for("index"))
        else:
            return render_template("index.html", error = "Username or password is incorrect")

    return render_template("index.html")
