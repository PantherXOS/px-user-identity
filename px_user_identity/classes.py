class UserDeviceAccountRegistration:
    def __init__ (self, public_key, title, location):
        self.public_key: str = public_key

class UserClass:
    def __init__(self, user_id, user_type, is_managed, first_name, last_name, email):
        self.id = user_id
        self.user_type = user_type
        self.is_managed = is_managed
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
