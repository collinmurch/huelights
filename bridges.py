import requests, os

#Scan network for all bridges (unix only)
def scan():
    #Look for specific mac address then cut out ip
    ips=os.popen('arp -na | grep 0:17:88 | cut -d "(" -f 2 | cut -d ")" -f 1').read().split('\n')
    ips.remove('')

    #Remove all further false positives
    for i in ips:
        r=requests.get('http://%s' %i)
        if 'philips' not in r.text:
            ips.remove(i)

    return ips

#Return token if link button has been pressed
def getToken(ip):
    r=requests.post('http://%s/api' %ip, data='{"devicetype":"huelights"}')
    if 'success' in r.text:
        return r.text.split('"', 6)[5]
    else:
        return ''
   
#See if token is valid -- used for debugging
def testToken(ip, token):
    r=requests.get('http://%s/api/%s' %(ip, token))
    if 'lights' in r.text:
        return True
    else:
        return False
    