import json
import sys
import requests
import pandas as pd
from getpass import getpass

#TAKE USER INPUT
def TakeUserInputDef():
    # taking the input from the user
    fmcNameUserInput = input("Enter FMC Hostname space-separated, press Enter once finish: ").upper()
    # spliting the data
    fmcNameUserInput = fmcNameUserInput.split()
    # printing the data
    print("You have entered: ",fmcNameUserInput, "DEF TakeUserInputDef")
    usernameRaw = input("Username: ")
    passwordRaw = getpass(prompt="Enter password: ",stream=None)
    # passwordRaw = input(f"Enter password for {usernameRaw}: ")
    return fmcNameUserInput, usernameRaw, passwordRaw


# username = "xsnspmfw"
# if len(sys.argv) > 1:
#     username = sys.argv[1]
# if len(sys.argv) > 2:
#     password = sys.argv[2]



#CombineFMCURL
def CombineFMCURLDef(fmchostnamevariable):
    fmcURLLogin=[]
    fmcURLGET=[]
    if fmchostnamevariable:
        # fmcURL = "https://" +  fmcHostname[i] + "/api/fmc_platform/v1/auth/generatetoken"
        for i in (range(len(fmchostnamevariable))):
            #EXTRACT USER INPUT AND APPEND WITH URL RESPECTIVELY
            fmcURLLoginAPI = "https://" + fmchostnamevariable[i] + auth_url
            fmcURLLogin.append(fmcURLLoginAPI)
            fmcURLGETAPI = "https://" + fmchostnamevariable[i] + api_path
            fmcURLGET.append(fmcURLGETAPI)
            #Return FMC Hostname and FMCURL
    #RETURN VALUE
    return fmcURLLogin,fmcURLGET,fmchostnamevariable

#SETTING HEADERS, NEXT REQUIREMENT WILL APPEND TOKEN TO IT
headers = {'Content-Type': 'application/json'}

#DECLARE VARIABLE
auth_token=[]
auth_url="/api/fmc_platform/v1/auth/generatetoken"
api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/devices/devicerecords?limit=400&expanded=true"
# new API SAMPLE = https://usdal-secfmc102/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/devices/devicerecords?expanded=true
api_path= "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/devices/devicerecords?expanded=true"
DeviceList=[]
totalErrorFMC=[]

#CALLING FUNCTION
#PASS URL AND FMC HOSTNAME

fmcHostname, username, password = TakeUserInputDef()
# print(username,password)
URL_Login,URL_GET,fmchostnamevariable = (CombineFMCURLDef(fmcHostname))

if len(fmchostnamevariable) == 0:
    print("no Input")
else:
    for i in  (range(len(fmchostnamevariable))):
        #INITIATE LOGIN
        try:
            r = requests.post(URL_Login[i], headers=headers, auth=(username,password), verify=False)
            #EXTRACT TOKEN AND APPEND TO HEADER
            headers['X-auth-access-token']=r.headers.get("X-auth-access-token")
            
            print("FMC Hostname is: ", fmchostnamevariable[i])
            print("URL Login is: ",URL_Login[i])
            print("URL GET is: ",URL_GET[i])
            print("Header is: ", headers)
            # token = headers.get("X-auth-access-token")
            token = headers['X-auth-access-token']
            print("Token is: ",token)

            #INITIATE GET CALL
            r=requests.get(URL_GET[i],headers=headers,verify=False)
            data=r.json()
            for j in data['items']:
                DeviceName=j['name'].upper()
                DeviceID=j['id']
                DeviceModel=j['model']
                DeviceSW=j['sw_version']
                DevicehealthStatus=j['healthStatus']
                try:
                    DeviceftdMode=j['ftdMode']
                except:
                    DeviceftdMode="N/A"
                try:
                    DeviceAccessPolicy=j['accessPolicy']['name']
                except:
                    DeviceAccessPolicy="N/A"
                try:
                    DevicehealthPolicy=j['healthPolicy']['name']
                except:
                    DevicehealthPolicy="N/A"
                DeviceIPAddress=j['hostName']
                try:
                    DevicedeviceGroup=j['deviceGroup']['name']
                except:
                    DevicedeviceGroup="N/A"
                DeviceInfo=[DeviceName,DeviceID,DeviceModel,DeviceSW,DevicehealthStatus,DeviceftdMode,DeviceAccessPolicy,DevicehealthPolicy,DeviceIPAddress,DevicedeviceGroup,fmchostnamevariable[i]]
                DeviceList.append(DeviceInfo)
                df = pd.DataFrame(DeviceList, columns= ['DeviceName','ID','Device Model','Software Version','Health Status','FTDMode','Access Policy','Health Policy','Imported using IP or Hostname','Device Group',"FMC"]) 
                df.to_csv ('CombineFMC.csv', index = False, header=True)  
                # print (df)
        except:
            errorFMC = fmchostnamevariable[i]
            totalErrorFMC.append(errorFMC)
        
    print("Total unreachable FMC  is",len(totalErrorFMC))
    print(totalErrorFMC)
                

