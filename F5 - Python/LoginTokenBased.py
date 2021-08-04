import requests
import json
from requests.auth import HTTPBasicAuth 



url="https://<f5hostname>/mgmt/shared/authn/login"
#SETTING HEADERS
headers= {
    'Content-Type': 'application/json'
}

badan = {
    "loginProviderName": "tmos",
    "username": "user",
    "password": "password"
}
responseF5 = requests.post(url,headers=headers,json=badan,verify=False)
responseJSONF5=responseF5.json()

print("Raw response is:", responseJSONF5)
print("Token is", responseJSONF5['token']['token'])


