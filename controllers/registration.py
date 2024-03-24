from flask import render_template,redirect,url_for,request
from models.registration import register_event_organizer

def register():

    if request.method == "POST":
        if register_event_organizer(event_id, data):
            
    else:
        return 