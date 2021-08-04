import requests
import json
import pandas as pd

UserListFile = r"C:\Users\xxx\Desktop\ScriptTest\License.csv"
SSLCert = r"C:\Users\xxxx\Desktop\xxxx.cer"
# sessionID = "a46c89ddd60010a2c15f064eb4e6183e"
sessionID = "ccff3c2791b8f66b3ca8d527f333266b"

#Calling the API function
def getUserList(session_ID):
    URL="https://urlurlm/afa/api/v1/license?domain=0"
    kepala={
        'Cookie':'PHPSESSID='+session_ID,
        } 
    r=requests.get(URL,headers=kepala,verify=False)
    data = r.json()
    #CONVERT INTO TABLE USING PANDA
    DataConvertedtoPanda = pd.DataFrame([data])
    print(DataConvertedtoPanda)
    #PRINT THE TABLE TO CSV
    DataConvertedtoPanda.to_csv (UserListFile, index = False, header=True)
    
    
    #Check HTTP response
    if r.status_code == 200:
        print ("Authentication successful, output printed into", UserListFile)
    else:
        print("HTTP error code is:", r.status_code)


    
getUserList("e56f5f0e54a61e8e6f32274870c90361")



# ################TO EXTRACT SPECIIC KEY PAIR
#  result={key: data[key] for key in data.keys() & {'License_type','Account_name'}}
#     print (result)
