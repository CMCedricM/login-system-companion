import os, sys 
import requests

url = "http://192.168.68.101:5150/signup"

def createUser(username, password):
    data = {
        "email": username,
        "password": password
    }
    print(f"Now Sending {data}")
    res = requests.post(url, json=data)
    if(res.ok): 
        return (True, None)
    else: 
        return (False, res.text)
