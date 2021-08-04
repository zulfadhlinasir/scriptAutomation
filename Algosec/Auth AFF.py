import requests
import json
import pandas as pd

UserListFile = r"C:\Users\xxxx\Desktop\ScriptTest\License.csv"
SSLCert = r"C:\xxx\xxxx\Desktop\xxx.cer"
# sessionID = "a46c89ddd60010a2c15f064eb4e6183e"
sessionID = "ccff3c2791b8f66b3ca8d527f333266b"

#Calling the API function
def getUserList(session_ID):
    # URL="https://urlurl/afa/api/v1/license?domain=0"
    URL="https://urlurl/FireFlow/api/authentication/authenticate"
    kepala={
        'Accept': '*/*',
        'Content-Type': 'application/json',
    }
    body={
        'username': 'pentest1',
        'password': 'blkbalbalb',
    }
    r=requests.post(URL,headers=kepala,data=json.dumps(body),verify=False)
    data = r.json()
    print(data["data"]["sessionId"])


    
getUserList("4626b67e400dbe236083e86a72444fd2")



# ################TO EXTRACT SPECIIC KEY PAIR
#  result={key: data[key] for key in data.keys() & {'License_type','Account_name'}}
#     print (result)
