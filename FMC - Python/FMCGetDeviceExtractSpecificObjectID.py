#Written by Zars Nov-9,2020
#This code is to extract FTD information via FMC API, display the output and also print it to "FMCHostname".csv file
#
 
import json
import sys
import requests
import pandas as pd
from getpass import getpass

# fmcName=input("Enter FMC Hostname (Case insensitive):")
# username = input("Please enter username:")
# password= print("Enter password for",username)
# password=getpass()

#Combining the FMC URL
server = "https://" + fmcName

username = "xsnspmfw"
if len(sys.argv) > 1:
    username = sys.argv[1]
password = "pD$bK72y@d4YC3FC"
if len(sys.argv) > 2:
    password = sys.argv[2]

               
r = None
headers = {'Content-Type': 'application/json'}
api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
auth_url = server + api_auth_path

try:
    # 2 ways of making a REST call are provided:
    # One with "SSL verification turned off" and the other with "SSL verification turned on".
    # The one with "SSL verification turned off" is commented out. If you like to use that then 
    # uncomment the line where verify=False and comment the line with =verify='/path/to/ssl_certificate'
    # REST call with SSL verification turned off: 
    r = requests.post(auth_url, headers=headers, auth=(username,password), verify=False)
    # REST call with SSL verification turned on: Download SSL certificates from your FMC first and provide its path for verification.
    # r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify=r"C:\Users\xxxxxx\Desktop\SSL Cert\FMCRootCe.cer")
    auth_headers = r.headers
    auth_token = auth_headers.get('X-auth-access-token', default=None)
    if auth_token == None:
        print("auth_token not found. Exiting...")
        sys.exit()
except Exception as err:
    print ("Error in generating auth token --> "+str(err))
    sys.exit()

headers['X-auth-access-token']=auth_token

# api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/devices/devicerecords"    # param
api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/devices/devicerecords?limit=300&expanded=true"
url = server + api_path

if (url[-1] == '/'):
    url = url[:-1]

# GET OPERATION
#Declaring a list to store the imported device name
DeviceList=[]
DeviceListDict={}
try:
    # REST call with SSL verification turned off: 
    r = requests.get(url, headers=headers, verify=False)
    # REST call with SSL verification turned on:
    # r = requests.get(url, headers=headers, verify=r'C:\Users\xxxxx\Desktop\SSL Cert\FMCRootCe.cer')
    status_code = r.status_code
    resp = r.text
    if (status_code == 200):
        print("GET successful. Printing the information for", fmcName.upper())
        data=r.json()
        print(r.json)
        DeviceNameCombine=[]
        DeviceIDCombine=[]
        for i in data['items']:
            DeviceName=i['name'].upper()
            DeviceID=i['id']
            DeviceModel=i['model']
            DeviceSW=i['sw_version']
            DevicehealthStatus=i['healthStatus']
            try:
                DeviceftdMode=i['ftdMode']
            except:
                DeviceftdMode="N/A"
            DeviceAccessPolicy=i['accessPolicy']['name']
            try:
                DevicehealthPolicy=i['healthPolicy']['name']
            except:
                DevicehealthPolicy="N/A"
            DeviceIPAddress=i['hostName']
            DevicedeviceGroup=i['deviceGroup']['name']
            DeviceInfo=[DeviceName,DeviceID,DeviceModel,DeviceSW,DevicehealthStatus,DeviceftdMode,DeviceAccessPolicy,DevicehealthPolicy,DeviceIPAddress,DevicedeviceGroup]
            DeviceList.append(DeviceInfo)
            
            # #To store for Dict
            # DeviceIDCombine.append(DeviceID)
            # DeviceNameCombine.append(DeviceName)

        # #Storing data into Dict    
        # DeviceListDict={'FTDName' : DeviceNameCombine , 'DeviceID' : DeviceIDCombine}
        # # print(DeviceListDict)

        #Print List in List and export to CSV
        df = pd.DataFrame(DeviceList, columns= ['DeviceName','ID','Device Model','Software Version','Health Status','ftdMode','Access Policy','Health Policy','Imported using IP or Hostname','Device Group'])
        df.to_csv (f'{fmcName}.csv', index = False, header=True)  
        print (df)
        print("Output printed to {}.csv".format(fmcName))

        
        
        #Extracting FTD Name
        combineActualFTD=[]
        selectFTDName=input("Enter FTD Hostname (Case insensitive):").upper()
        print("Looking for FTD Name",selectFTDName,"....")
        for i in DeviceList:
            if(selectFTDName in i[0]):
            # if(i[0]==selectFTDName):
                actualFTD = (i[0],i[1])
                combineActualFTD.append(actualFTD)
                # print(i[0],i[1])

        #Printout matching FTD Name
        numberOfFTD =(len(combineActualFTD))
        if (numberOfFTD==0):
            print("No FTD name found!")
        elif (numberOfFTD==1):
            print("FTD Name is",combineActualFTD[0][0])
            print("Object ID is",combineActualFTD[0][1])
        else:
            print("Please redefine your search, there are", numberOfFTD, "devices having similar name")
            print("Those devices are:")
            for i in combineActualFTD:
                print(i[0])
                
            
    else:
        r.raise_for_status()
        print("Error occurred in GET --> "+resp)
except requests.exceptions.HTTPError as err:
    print ("Error in connection --> "+str(err)) 
finally:
    if r : r.close()

