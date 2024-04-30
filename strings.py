EMAIL_PASSWORD_EMPTY = {
    "success": False,
    "message": "Email and Password cannot be empty!",
}
INVALID_PASSWORD = {"success": False, "message": "Password is Incorrect!"}
INVALID_EMAIL = {"success": False, "message": "Email is Incorrect!"}

LOGIN_SUCESS = {"success": True, "message": "Login Sucess!"}
LOGOUT_SUCESS = {"success": True, "message": "Logout Sucessfully!"}
REGISTRATION_SUCESS = {"success": True, "message": "Registered Sucessfully!"}
BAD_CREDENTIALS = {"success": False, "message": "Bad Credentials"}
UNAUTHORIZED = {"success": False, "message": "Unauthorized access"}

# Event Organizer data

NAME_EMPTY = {"success": False, "message": "Name is required!"}
ADDRESS_EMPTY = {"success": False, "message": "Address is required!"}
EMAIL_EMPTY = {"success": False, "message": "Email is required!"}
PASSWORD_EMPTY = {"success": False, "message": "Password is required!"}
STATUS_EMPTY = {"success": False, "message": "Status is required!"}
EMAIL_EXISTS = {"success": False, "message": "Username already exists!"}

# Events
NO_EVENTS = {"success": False, "message": "No Events at the moment"}
EVENT_DOESNT_EXIST = {"success": False, "message": "Event does not exist."}
EVENT_NAME_EMPTY = {"success": False, "message": "Event name is required!"}
EVENT_DATE_EMPTY = {"success": False, "message": "Event date is required!"}
EVENT_EXISTS = {"success": False, "message": "Event already existed!"}
EVENT_SUCESS = {"success": True, "message": "Event created sucessfully!"}
EVENT_RETRIEVED = {"success": True, "message": "Events retrieved successfully"}
UPDATE_EVENT = {"succces": True, "message": "Update event successfully!"}
FAILED_UPDATE = {"succces": False, "message": "Unable to update event!!"}
DELETED_EVENT = {"success": True, "message": "Successfully deleted event!"}
FAILED_DELETE = {"success": False, "message": "Unable to delete event!"}


# Photographer
PHOTOGRAPHER_EXISTS = {"success": False, "message": "Photographer already registered!"}
PHOTOGRAPHER_REGISTERED_SUCCESSFULLY = {
    "success": True,
    "message": "Photographer reigstered sucessfully!",
}
GET_PHOTOGRAPHERS = {"success": True, "message": "Photographers retrieved successfully"}
NO_PHOTOGRAPHERS = {
    "success": False,
    "message": "No registered photographers at the moment",
}


# Runner
FIRST_NAME_EMPTY = {"success": False, "message": "First name is required!"}
LAST_NAME_EMPTY = {"success": False, "message": "Last name is required!"}
BIB_NO_EMPTY = {"success": False, "message": "BIB Number is required!"}
RUNNER_REGISTRATION_SUCCESSFUL = {
    "success": True,
    "message": "Runner registered sucessfully!",
}
NO_RUNNERS = {"success": False, "message": "No Runners registered at the moment"}
NO_SINGLE_RUNNER = {"success": False, "message": "Runner doesn't exists"}
RUNNERS_FETCHED = {"success": True, "message": "Successfully feteched all runners!"}
ONE_RUNNER_FETHCED = {"success": True, "message": "Successfully feteched a runner!"}


# Upload Image
NO_IMAGES_INSERTED = {"message": "No inserted images"}
IMAGE_SUCCESS = {"message": "Uploaded images successfully"}
