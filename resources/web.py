import os, sys
import string
from tokenize import String 
import requests

url = "http://localhost:5150"
urlSignUp = f"{url}/signup"
urlLogin = f"{url}/loginAPI"
urlLogout = f"{url}/logoutAPI"

def createUser(username, password):
    data = {
        "email": username,
        "password": password
    }
    res = requests.post(url, json=data)
    if(res.ok): 
        return (True, None)
    else: 
        return (False, res.text)


def loginUser(username, password): 
    data = {
        'email':username, 
        'password':password
    }
    
    try: 
        res = requests.post(urlLogin, json=data) 
        if(res.ok): 
            return (True, res.text)
        else: 
            return (False, res.text)
    except Exception as e: 
        return(False, "Server Error, Try Again Later!")
    
    
def logoutUser() -> tuple[bool,String]: 
    try:
        res = requests.get(urlLogout)
        if(res.ok): 
            return (True, '') 
        else: 
            return (False, res.text)
    except Exception as e: 
        return(False, "Server Error!")
    
    
    