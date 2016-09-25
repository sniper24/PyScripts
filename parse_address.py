# coding=utf-8
import numpy as np
import pandas as pd
import re
import random
import requests
import time
###################################DataFrame###################

filename="d:\\deliverytest.csv"
start=0
end=4999


df=pd.read_csv(filename)
#df=pd.read_csv("d:\\deliverydata.csv")
df["formatted_address"]=["" for i in range(len(df))]
df["lat"]=[0.0 for i in range(len(df))]
df["lng"]=[0.0 for i in range(len(df))]

###############################################################     

onesecondflag=False # Not so sure
proxylist=[]
ualist=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60','Opera/8.0 (Windows NT 5.1; U; en)','Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0']
currentUseragent=""
def switchUseragent():
    print "switched to next UA"
    return random.choice(ualist)
                
def getProxies():
    # http://proxy.com.ru/list_1.html
    proxylist=[]
    
    pattern=re.compile(r'<tr><b><td>\d+</td><td>(?P<proxy>\d+\.\d+\.\d+\.\d+)</td><td>(?P<port>\d+)</td><td>.+</td><td>.+</td></b></tr>')
        
    for i in range(7):
        r = requests.get("http://proxy.com.ru/list_%d.html" %(i+1))
        result=pattern.findall(r.text)
        resultlist=[":".join(result[i]) for i in range(len(result))]   
        proxylist+=resultlist            
    return proxylist   

def switchProxy():
    proxyline=random.choice(proxylist)
    proxies = {"http": "http://%s"%proxyline}
    print "switching to next proxy"
    return proxies        
                        
def cleanAddress(addr):#dirtyAddr cleanAddr
# ** 1234-5678    12345678
    p1=re.compile(r'\d{8}')#12345678
    addr=p1.sub('',addr)
    
    p2=re.compile(r'\d{4}-\d{4}') #1234-5678
    addr=p2.sub('',addr)
    
    p3=re.compile(r'\(.*\)')  #
    addr=p3.sub('',addr)
    
    p4=re.compile(r'\*+.+\*+')#
    addr=p4.sub('',addr)
    
    p5=re.compile(r'(, )+')   #
    addr=p5.sub(', ',addr)  
    
    return addr
    
def splitAddress(clean_addr):
    addrlist=re.compile(r', *').split(clean_addr)#
    return addrlist

def pullGeocoding(addrlist):
    for i in range(len(addrlist)-1):
        pullString=", ".join(addrlist[-i-2:])#
        print pullString
        geocodinglist=getGeocoding(pullString)
        if geocodinglist:
            print "depth=%d+2"%i
            return geocodinglist
            
    return False        
        
def getGeocoding(addr):
    global currentProxy
    global onesecondflag
    global currentUseragent
    params1 = dict(address=addr)
    headers = {'User-Agent': currentUseragent,region="HK"} # This is another valid field
    	
    while True:
        try:
            r = requests.get('http://maps.googleapis.com/maps/api/geocode/json', params=params1,proxies=currentProxy,headers=headers).json()
            break
        except requests.exceptions.ConnectionError:
            print "Connection Error...Waiting for a new proxy"
            currentProxy=switchProxy()
            print "Switched to a new proxy"
        except requests.exceptions.Timeout:
            print "Connection Timeout...Waiting for a new proxy"
            currentProxy=switchProxy()
            print "Switched to a new proxy"
       
    if r['status']=='OK':
        onesecondflag=False
        address_info=[r['results'][0]['formatted_address'],float(r['results'][0]['geometry']['location']['lat']),float(r['results'][0]['geometry']['location']['lng'])]
        return address_info#list
    elif r['status']=='ZERO_RESULTS':
        onesecondflag=False
        return False  #False
    
    elif r['status']=='OVER_QUERY_LIMIT':
        if onesecondflag:
            print "Query Limit has been reached...switching to another proxy."
            currentProxy=switchProxy()
            currentUseragent=switchUseragent()
            print "Switched to a new proxy"
            returnValue=getGeocoding(addr)
        else:
            time.sleep(1)
            onesecondflag=True
            returnValue=getGeocoding(addr)
        return returnValue

#############################Main programme start######################################        
                        
proxylist=getProxies() #get original proxies

print "Original proxy list %d proxies"%(len(proxylist))
                                              
currentProxy=switchProxy()  #
print "First proxy ready"

currentUseragent=switchUseragent()
print "First UA ready"


#for i in range(len(df)):
for i in range(end-start):
    addr=df.SHIP_ADDR[i+start]
    
    clean_addr=cleanAddress(addr)
    
    addrlist=splitAddress(clean_addr) 
    print "Processing %d th address"%(i+start)   
    df.iloc[(i+start),-3:]=pullGeocoding(addrlist)
    print "%d th address processed"%(i+start)
    print df.iloc[(i+start),-3:]
#df.to_csv("d:\\deliverydata1.csv",index_label=False)
df.to_csv(filename,index_label=False)