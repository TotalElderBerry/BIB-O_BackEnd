from flask import render_template,redirect,url_for,request
from models.login import login_event_organizer
from strings import (LOGIN_SUCESS, 
                     EMAIL_DOES_NOT_EXIST, 
                     INVALID_PASSWORD,
                     EMAIL_PASSWORD_EMPTY)

def login():

    if request.method == "POST":

        if login_event_organizer() == 1: 
            return redirect(url_for("index"), message = LOGIN_SUCESS)
        elif login_event_organizer == 2:
            return render_template("index.html", message = EMAIL_DOES_NOT_EXIST)
        elif login_event_organizer == 3:
            return render_template("index.html", message = INVALID_PASSWORD)
        else: 
            return render_template("index.html", message = EMAIL_PASSWORD_EMPTY)

    print(EMAIL_PASSWORD_EMPTY)
    return render_template("index.html")
