from flask import render_template,redirect,url_for
from models.login import login_event_organizer

def login(data):

    