import requests
import re





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
    
    
proxylist=getProxies()

with open('D:\\0622\\proxylist.txt', 'a') as the_file:
    for i in range(len(proxylist)):
        the_file.write(proxylist[i]+'\n')
        
        
the_file.close()

