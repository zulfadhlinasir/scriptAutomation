import json
import requests
import pandas as pd
from getpass import getpass
from requests.auth import HTTPBasicAuth 

#SETTING HEADERS
headers = {'Content-Type': 'application/json'}

#DECLARE VARIABLE
user="xxxdx"
password="xxxxx"

poolState_URL="https://<f5Hostname>/mgmt/tm/ltm/pool/"
inventory_Path="inventory.txt"

#Declare File
poolInfoFile='PoolInformation.csv'
failedF5File='failedF5.csv'


#initialize array to store information
poolInfoCombine=[]
poolLinkCleanedCombine=[]
inventoryList=[]
rawDataPoolNameCombine=[]
failedHostname=[]

#DECLARE FUNCTION TO EXTRACT HOSTNAME FROM FEED FILE
def extractHostname():
    readInventory=open(inventory_Path,"r")
    for j in readInventory:
        stripFile=j.strip()
        inventoryList.append(stripFile)
    return inventoryList

#EXTRACT POOLNAME AND SANITIZE+RETURN THE API URI TO BE CALLED LATER ON
def getPoolName(inventoryList,userName,passWord):
    for hostname in inventoryList:
        poolName_URL= "https://" + hostname + "/mgmt/tm/ltm/pool/"
        try:
            rPoolName = requests.get(url=poolName_URL,headers=headers, auth = HTTPBasicAuth(userName,passWord),verify=False) 
            rawDataPoolName=rPoolName.json()
            for j in rawDataPoolName['items']:
                poolName=j['name']
                poolLink=j['selfLink']
                #FILTER URL
                poolLinkCleanedReplaceLocalHost = poolLink.replace("localhost",hostname)
                poolLinkCleanedRemoveURIath=poolLinkCleanedReplaceLocalHost.split("?")[0]
                poolLinkCleanedAddMembers=poolLinkCleanedRemoveURIath + "/members"
                #Appending Hostname into the Array
                poolLinkCleanedAddHostname=[poolLinkCleanedAddMembers,hostname]
                poolLinkCleanedCombine.append(poolLinkCleanedAddHostname)
        except:
            print ("unable to reach information from", hostname)
            failedHostname.append(hostname)  
    #Extract deviced failed to be reached, and copy into CSV file
    df = pd.DataFrame(failedHostname, columns= ['Device failed to be reach']) 
    df.to_csv (failedF5File, index = False, header=True)
    print  (df)
    return (poolLinkCleanedCombine)

#MAKE API CALL USING URL SUPPLIED IN FUNCTION geetPoolName AND EXTRACT NECESSARY INFORMATION
def getPoolInfo(poolLinkCleanedCombine,userName,passWord):
    for j in poolLinkCleanedCombine:
        #poolLinkCleanedCombine have 2 variables, 0th element contains URL while 1st element will be inserted Hostname
        rPoolState = requests.get(url=j[0],headers=headers, auth = HTTPBasicAuth(userName,passWord),verify=False)
        #insert F5 hostname into 2nd element of poolLinkCleanedCombine
        hostname = (j[1])
        try:
            rawPoolState=rPoolState.json()
            for j in rawPoolState['items']:
                memberIP=j['address']
                memberState=j['state']
                memberPort=j['name']
                poolName=j['selfLink']
                poolNameCleanedA=poolName.split("/")[7]
                poolNameCleaned=poolNameCleanedA.split("Common~")[1]
                #append all infromation including hostname (j['1'])
                poolInfoCollect=[poolNameCleaned,memberIP,memberState,memberPort,hostname]
                poolInfoCombine.append(poolInfoCollect)
        except:
            print("Unable to print information")
    return poolInfoCombine    

inventoryList=extractHostname()
rawDataPoolNameCombine=getPoolName(inventoryList,user,password)
poolInfoCombine=getPoolInfo(poolLinkCleanedCombine,user,password)

#PRINT THE POOL MEMBER INFORMATION INTO CSV FILE
df = pd.DataFrame(poolInfoCombine, columns= ['Pool Name','IP Address','State','Address/Name and Port', 'hostname']) 
df.to_csv (poolInfoFile, index = False, header=True)  
print (df)
            



    



