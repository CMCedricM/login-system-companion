import os, sys 
import requests

url = "http://localhost:5150/signup"
urlLogin = "http://localhost:5150/loginAPI"

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
    
    res = requests.post(urlLogin, json=data) 
    if(res.ok): 
        return (True, res.text)
    else: 
        return (False, res.text)
    