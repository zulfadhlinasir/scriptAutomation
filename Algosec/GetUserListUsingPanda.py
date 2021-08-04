import requests
import json
import pandas as pd

UserListFile = r"C:\Users\xxx\Desktop\ScriptTest\UserList.csv"
SSLCert = r"C:\Users\xxxxx\Desktop\xxxx.cer"
sessionID = "1vbgpdh41dr5gbrrl4i34tldf1"


#Calling the API function
def getUserList(session_ID):
    URL="https://<fmc hottname>/afa/api/v1/users"
    kepala={
        'Cookie':'PHPSESSID='+session_ID,
        } 
    r=requests.get(URL,headers=kepala,verify=False)
    #Check HTTP response
    if r.status_code == 200:
        print ("Authentication successful, output printed into", UserListFile)
    else:
        print("HTTP error code is:", r.status_code)
    
    #CONVERT RESPONSE INTO JSON FORMAT
    data=r.json()
    #GO 1 LEVEL DEEPER INTO KEY USER
    newData = data['users']
    #CONVERT DATA INTO TABLE USING PANDAS WITH RESPECTIVE COLUMN HEADER
    result=pd.DataFrame(newData).reindex(columns=['UserName','FullName','Email','Roles','AuthenticationType','Administrator','FireflowAdmin','AllowedActions'])
    result.to_csv (UserListFile, index = False, header=True) 

    
###CALLING FUNCTION    
getUserList(sessionID)






    






