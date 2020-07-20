class UserDeviceAccountRegistration:
    def __init__ (self, public_key, title, location):
        self.public_key: str = public_key

class RequestedOperation:
    def __init__(self, action: str, security: str, key_type: str, force_operation: bool = False):
        self.action = action
        self.security = security
        self.key_type = key_type
        self.force_operation = force_operation

class UserClass:
    def __init__(self, user_type, is_managed, first_name, last_name, email):
        self.user_type = user_type
        self.is_managed = is_managed
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
