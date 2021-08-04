import requests

###########################Z
import csv
import pandas as pd

device_uri = 'urlrurl/afa/api/v1/devices'
fileA = r"C:\Users\mzbnasi\Desktop\ScriptTest\FirewallDataXMLTOCSV.csv"

def Get_Device_List(sess_ID):

    ###########################Z
    
    header_device = {
        # 'Content-Type': 'application/json',
        'Accept': '*/*',
        'Cookie': 'PHPSESSID=' + sess_ID
    }

    x = requests.get(device_uri, headers=header_device, verify=False).json()

    
    ###########IMPORTING TO CSV
    # df = pd.DataFrame(x)
    # df.to_csv(fileA, index = False) 
     
    #EMPTY LIST TO STORE FIREWALL NAME
    AllFW = []  
    FTDList = []
    remoteAgent = []
    ftdcount=0
    for i in x:
        #DECLARING PARENT FIREWALL NAME AND MAKE IT UPPPERCASE
        deviceName=i['name'].upper()
        # parent = deviceName
        AllFW.append(deviceName)
        #OPTIONAL - RECORD REMOTE AGENT
        remoteAg=i['collector']
        remoteAgent.append(remoteAg)
    
        #FILTER FTD
        if i['nodeType'] == "FW_MGMT":
            for j in i['firewallDataEntities']:
                FTDName = j['original_name'].upper()
                FTDList.append(FTDName)
                ftdcount = ftdcount + 1
    
    
    ALL = AllFW + FTDList
    #PRINT DATA INTO CSV
    # df = pd.DataFrame(data={"FirewallName": AllFW, "RemoteAgent": remoteAgent})
    df = pd.DataFrame(data={"FirewallName": ALL})
    df.to_csv(fileA,sep=',',index=False)     
    # with open(fileA,'a',newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(FTDName)
    # print(totalFTD)     
    #COUNT FMC 
    countFMC = ALL.count("FMC")     
    print("Total parent device is:", len(AllFW))
    print("FMC count: ", countFMC)
    print("FTD Count: ", len(FTDList))
    print("Total imported device is (Minus FMC and add FTD):", len(AllFW) - countFMC + len(FTDList))
    


Get_Device_List("445aff8d403cd6fd554ec3af3ad12bfc")
