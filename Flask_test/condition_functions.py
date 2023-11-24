import re

def check_username_conditions(username):        
    if ' ' in username:
        return False
    elif len(username) < 8 or len(username) > 20:
        return False
    else:
        return True

def check_password_conditions(password):
    if ' ' in password:
        return False
    else:
        if len(password) < 8 and len(password) > 20:
            return False
        elif bool(re.search(r'[A-Z]', password)) and bool(re.search(r'[a-z]', password)):
            if bool(re.search(r'[0-9]', password)):
                if bool(re.search(r'[^a-zA-Z0-9_]', password)):
                    return True
                else: return False
            else: return False
        else: return False