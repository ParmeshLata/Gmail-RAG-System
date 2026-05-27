from dotenv import set_key
import os

def save_credentials(email, password):
    if not email or not password:
        return "Please enter both email and password."
    
    env_file = '.env'
    
    if not os.path.exists(env_file):
        open(env_file, 'w').close()
    
    set_key(env_file, 'EMAIL', email)
    set_key(env_file, 'PASSWORD', password)
    
    return f"Credentials saved successfully!\nEMAIL: {email}\nPASSWORD: {'*' * len(password)}"