from database import engine
from sqlalchemy import text
from flask import session

def login_event_organizer(data):

    print(engine)
    with engine.connect() as conn:
    
        query = text("SELECT * FROM event_organizer WHERE email = :email")
        dict_text = dict(email = data["email"])

        result = conn.execute(query,dict_text)

        rows = result.fetchone()

        if rows[4] == data["email"] and rows [5] == data["password"]:
            session["username"] = data["email"]
            return 1
        elif rows[4] is not data['email']:
            return 2
        elif rows[4] is not data['password']:
            return 3
        else:
            return -1

            
            
        
        



    
