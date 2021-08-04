import csv
import xml.etree.ElementTree as ET
# import pandas
file = "firewall_data.xml"
fileA = "FirewallDataXMLTOCSV.csv"
fileB = "FirewallGroupXMLToCSV.csv"
fileC = "FirewallContextXMLToCSV.csv"



tree = ET.parse(file)
root = tree.getroot()
myData = []
myGroup = []
myContext = []

#Extract Normal Data
def extractNormalData():
    hostname = subchild.attrib.get("host_name")
    display = subchild.attrib.get("display_name")
    collector = subchild.attrib.get("collector")
    log_host_name = subchild.attrib.get("log_host_name")
    log_frequency = subchild.attrib.get("log_collection_frequency")
    monitoring = subchild.attrib.get("monitoring")
    brand_name = subchild.attrib.get("brand_name")
    brand = subchild.attrib.get("brand")
    baseline_profile = subchild.attrib.get("baseline_profile")
    collect_log_from_adt = subchild.attrib.get("collect_log_from_adt")
    data=[hostname,display,collector,log_host_name,monitoring,log_frequency,brand_name,brand,baseline_profile,collect_log_from_adt]
    myData.append(data)
    for subsubchild in subchild:
        if(subsubchild.tag=="FW_GEN"):
            FTDName = subsubchild.attrib.get("original_name")
            host_name = subsubchild.attrib.get("host_name")
            Collector = subsubchild.attrib.get("collector")
            Blankspace = ""
            Monitoring = subsubchild.attrib.get("monitoring")
            BrandName  = subsubchild.attrib.get("brand_name")
            Brand   = subsubchild.attrib.get("brand")
            FTD=[FTDName,host_name,Collector,Blankspace,Monitoring,Blankspace,BrandName,Brand]
            myData.append(FTD)

#Extract Group Data
def extractGroup():  
    for subsubchild in subchild:
        groupname = subchild.attrib.get("display_name")
        name = subsubchild.attrib.get("display_name")
        groupData=[groupname,name]
        myGroup.append(groupData)

#Extract Context Data
def extractContext():
    for subsubchild in subchild:
        if (subsubchild.tag == "CONTEXT"):
            displayName = subsubchild.attrib.get("display_name")
            contextData = [displayName]
            myContext.append(contextData)


#Looping thru the XML File
for child in root:
        for subchild in child:
            if (child.tag == "FIREWALLS"):
                extractNormalData()
                extractContext()
            elif  (child.tag == "GROUPS"):
                extractGroup()
               
####PRINT FIREWALDATA
def printNormalData():
    #Creating Header
    with open(fileA,'w') as f:
            f.write("Hostname" + ',' + "Display Name" + ',' + "Remote Agent" + ',' + "Collector" + ',' + "Monitoring Enabled?" + ',' + "Monitoring Frequency" + ',' + "Brand_name" + ','+ "Brand" + ',' + "Baseline Profile" + ',' + "collect_log_from_adt" +'\n')

    #Printing the input to CSV
    with open(fileA,'a') as f:
        for row in myData:
            for x in row:
                f.write(str(x) + ',')
            f.write('\n')
          
#####PRINT FIREWALL GROUP
def printFirewallGroup():
    with open(fileB,'w') as f:
        f.write("Group" + ',' + "Display Name" + '\n')
    #Printing the input to CSV
    with open(fileB,'a') as f:
        for row in myGroup:
            for x in row:
                f.write(str(x) + ',')
            f.write('\n')

def printContext():    
    with open(fileC,'w') as f:
        for row in myContext:
            for x in row:
                f.write(str(x) + ',')
            f.write('\n')

#Calling function                
extractNormalData()
extractGroup()
extractContext()


#Printing Output
printFirewallGroup()
printNormalData()
printContext()












         
        
       



