from flask import request


class event_organizer_obj:

    def __init__(self, event_id, name, address, email, password, status):
        self.event_id = event_id
        self.name = name
        self.address = address
        self.email = email
        self.password = password
        self.status = status
