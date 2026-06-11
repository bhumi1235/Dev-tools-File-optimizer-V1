class User:

    def __init__(self):
        self.name = "admin"


def authenticate(email, password):

    token = "jwt_token"

    return token


def logout():

    return True


def hash_password(password):

    return "hashed_" + password