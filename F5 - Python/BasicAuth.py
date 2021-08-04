import requests
from requests.auth import HTTPBasicAuth 

#SETTING HEADERS
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic <encodedBase64string> '
            }

url="https://IPADDRESS/mgmt/tm/ltm"
PoolName = requests.get(url=url,headers=headers,verify=False) 

print(PoolName.json())
