# -*- coding: utf-8 -*-
import requests
import re

proxylist=[]
print "Program initiating"
for i in range(30):
    try:
        r=requests.get("http://proxylist.hidemyass.com/%d#listable"%(i+1))
        print "Loading %d th page of proxies, please wait"%(i+1)
        text1=r.text
    except:
        print "%d th page loading error"%(i+1)
        pass
    
    pattern=re.compile(r"<td><span><style>(?P<shelter>.+?)</style>(?P<originalIP>.+?)</span></td>.*?<td>(?P<port>.+?)</td>",re.S)
    
    resultlist=pattern.findall(r.text,re.S)
    
    for j in range(len(resultlist)):
        #split the resultlist into 3 parts
        
        shelter=resultlist[j][0]
        originalIP=resultlist[j][1]
        port=resultlist[j][2]
        
        
        #shelter [none]
        patternShelter=re.compile(r"(\w+)\{display\:none\}",re.S)
        shelterlist=patternShelter.findall(shelter)#get the list for none shelter list

        
        for k in range(len(shelterlist)):
            patternShelterFilter=re.compile(shelterlist[k],re.S)
            originalIP=patternShelterFilter.sub("display:none",originalIP)#sub none shelter list with none

        
        #shelter [inline]
        patternShelter2=re.compile(r"(\w+)\{display\:inline\}",re.S)
        shelterlist2=patternShelter2.findall(shelter)#get the list for none shelter list

        
        for k in range(len(shelterlist2)):
            patternShelterFilter2=re.compile(shelterlist2[k],re.S)
            originalIP=patternShelterFilter2.sub("display: inline",originalIP)#sub none shelter list with none

        
        #numeric shelter[123]
        patternShelter3=re.compile(r"<span class=\"\d+\">")
        originalIP=patternShelter3.sub("<span class=\"display: inline\">",originalIP)
        
        
        #2nd round shelter -- to delete"<span style="c2-display: inline"> prefix

        secondFilter1=re.compile(r"<span style=\"\w+-display: inline\">")
        originalIP=secondFilter1.sub("<span style=\"display: inline\">",originalIP)
        
        secondFilter2=re.compile(r"<span style=\"\w+-display:none\">")
        originalIP=secondFilter2.sub("<span style=\"display:none\">",originalIP)
        
        secondFilter3=re.compile(r"<span class=\"\w+-display: inline\">")
        originalIP=secondFilter3.sub("<span class=\"display: inline\">",originalIP)
        
        secondFilter4=re.compile(r"<span class=\"\w+-display:none\">")
        originalIP=secondFilter4.sub("<span class=\"display:none\">",originalIP)

        
        ipFilter=[]
        ipFilter.append(re.compile(r"<span class=\"display:none\">.+?</span>",re.S))
        ipFilter.append(re.compile(r"<div style=\"display:none\">.+?</div>",re.S))
        ipFilter.append(re.compile(r"<span style=\"display:none\">.+?</span>",re.S))
        
        for p in range(3):
            originalIP=ipFilter[p].sub("",originalIP)
 
        ipPattern=re.compile(r"[\d\.]+")
        ipList=ipPattern.findall(originalIP)
        
        if len(ipList)==7:
            ip="".join(ipList)
            
            port=re.compile(r"\s").sub("",port)
            proxy=ip+":"+port
            proxylist.append(proxy)

print proxylist
        
        
    #仍为解决的问题
    #1. 某些正确ip段被忽略
    #2. 掩码中有数字 进入了ip段中
           
with open('c:\\Users\\bojunxie2\\Downloads\\proxylist.txt', 'a') as the_file:
    for i in range(len(proxylist)):
        the_file.write(proxylist[i]+'\n')
        
        
the_file.close()    
           
                    