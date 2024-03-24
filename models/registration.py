from database import engine
from sqlalchemy import text


def register_event_organizer(event_id,data):

    with engine.connect() as conn:

        query = text("INSERT INTO event_organizer(event_id,name,address,email,password,status) VALUES(:event_id,:name,:address,:email,:password,:status)")
        parameters = dict(event_id = event_id, 
                          name = data['name'], 
                          address = data['address'], 
                          email = data['email'], 
                          password = data['password'], 
                          status = data['status'])
        
        result = conn.execute(query,parameters)
    
        conn.commit()
