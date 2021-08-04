import requests
import json
import pandas as pd

UserListFile = r"C:\Users\xx\Desktop\ScriptTest\UserList.csv"
SSLCert = r"C:\Users\xx\Desktop\xxx.cer"
# sessionID = "a46c89ddd60010a2c15f064eb4e6183e"
sessionID = "4bdb59964ef00c4d95ec8636c86d9b5e"

combine={}
#Calling the API function
def getUserList(session_ID):
    URL="https:/<fmchostname>/afa/api/v1/users"
    kepala={
        'Cookie':'PHPSESSID='+session_ID,
        } 
    r=requests.get(URL,headers=kepala,verify=False)
    #Check HTTP response
    if r.status_code == 200:
        print ("Authentication successful, output printed into", UserListFile)
    else:
        print("HTTP error code is:", r.status_code)
    
    xData = []
    #CONVERT RESPONSE INTO JSON FORMAT
    data=r.json()
    newData = data['users']
    for i in newData:
        for j in i['AuthorizedDevices']:
            print(i['UserName'],j['DisplayName'])
            # print(j['DisplayName'])
            
            
        


    #GO 1 LEVEL DEEPER INTO KEY USER
    # newData = data['users']
    # #CONVERT DATA INTO TABLE USING PANDAS WITH RESPECTIVE COLUMN HEADER
    # result=pd.DataFrame(newData).reindex(columns=['UserName','FullName','Email','Roles','AuthenticationType','Administrator','FireflowAdmin','AllowedActions'])
    # result.to_csv (UserListFile, index = False, header=True) 


###CALLING FUNCTION    
getUserList(sessionID)







    






