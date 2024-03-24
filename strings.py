
class CustomError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

EMAIL_PASSWORD_EMPTY = CustomError("Email or Password cannot be empty!", 400)
INVALID_CREDENTIALS = CustomError("Invalid Email or Password!", 400)
USERNAME_EXISTS = CustomError("Username already exists!", 400)
LOGIN_SUCESS = CustomError("Login Sucess!", 200)
