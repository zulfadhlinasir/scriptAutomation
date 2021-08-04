import requests
import json

UserListFile = r"C:\Users\xxxx\Desktop\ScriptTest\UserList.csv"
SSLCert = r"C:\Users\xxxx\Desktop\xxxx.cer"
sessionID = "ccff3c2791b8f66b3ca8d527f333266b"

#Declare empty list to append data
combineUserData =[]

##Declare a function to clean special char
def replaceMultiple(mainString, specialChar, newString):
    # Iterate over the strings to be replaced
    for elem in specialChar :
        # Check if string is in the main string
        if elem in mainString :
            # Replace the string
            mainString = mainString.replace(elem, newString)
    
    return  mainString


#Calling the API function
def getUserList(session_ID):
    URL="https://<fmc hostname./afa/api/v1/users"
    kepala={
        'Cookie':'PHPSESSID='+session_ID,
        } 
    r=requests.get(URL,headers=kepala,verify=False)
    
    #Check HTTP response
    if r.status_code == 200:
        print ("Authentication successful, output printed into", UserListFile)
    else:
        print("HTTP error code is:", r.status_code)

    data=r.json()

    for i in data['users']:
        UserName = (i['UserName'])
        FullName = (i['FullName'])
        #Need to join FullName because its comma separated
        jointFullName = FullName.replace(",","")
        Email = (i['Email'])

        try:
            Roles = (i['Roles'])
        except:
            Roles = ['None']

        #Need to join Roles because its comma separated
        jointRole = ' '.join(Roles)
        AuthenticationType = (i['AuthenticationType'])
        Administrator = (i['Administrator'])
        FireflowAdmin = (i['FireflowAdmin'])
        AuthorizedDevices = (i['AuthorizedDevices'])
        #ConvertAuthorizedDevice from LIST to STRING
        strAuthorizedDevices = str(AuthorizedDevices)
        #Replace Special Char
        stringAuthorizedDevices = strAuthorizedDevices.replace("[{'ID':","").replace("'","").replace("}]","").replace("]","")
        AllowedActions = (i['AllowedActions'])
        #Conver AllowedActions to STRING
        strAllowedActions=str(AllowedActions)
        #Cleanup AllowedActions
        # cleanAllowedActions=strAllowedActions.replace("['","").replace("'","").replace("']","")
        #Calling replaceMultiple function to clean special char
        cleanAllowedActions=replaceMultiple(strAllowedActions,['[',"'","']","]"], "")
        userData = [UserName,jointFullName,Email,jointRole,AuthenticationType,Administrator,FireflowAdmin,stringAuthorizedDevices,cleanAllowedActions]
        combineUserData.append(userData)
        # print(combineUserData)
        
#PRINT USER LIST
def printUserList():
    #Creating Header
    with open(UserListFile,'w') as f:
            f.write("UserName" + ',' + "FullName " + ',' + "Email" + ',' + "Roles" + ',' + "AuthenticationType" + ',' + "Administrator" + ',' + "FireflowAdmin" + ',' +  "AuthorizedDevices" + ',' + "AllowedActions" +'\n')

    #Printing the input to CSV
    with open(UserListFile,'a') as f:
        for row in combineUserData:
            for x in row:
                f.write(str(x) + ',')
            f.write('\n')


    
   

###CALLING FUNCTION    

getUserList(sessionID)

#PrintOutput
printUserList()




    






