from database import engine
from sqlalchemy import text
from flask import session


def login_event_organizer(data):

    with engine.connect() as conn:
        
        if data["email"] or data["password"] is None:
            return 
        # if data['email'] and data['password'] is not None:

            query = text("SELECT * FROM event_organizer WHERE email = :email")
            dict_text = dict(email = data["email"])

            result = conn.execute(query,dict_text)

            rows = result.fetchone()

            if rows[4] == data["email"] and rows [5] == data["password"]:
                session["username"] = data["email"]
                return True
            else:
                return False
   
            
            
        
        



    
