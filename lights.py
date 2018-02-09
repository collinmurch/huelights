import time,requests,json

data=json.load(open('lightsdata.json'))

token1=data['tokens']['1']
ip1='http://%s' %data['ips']['1']

token2=data['tokens']['2']
ip2='http://%s' %data['ips']['2']

name1=data['names']['1']
name2=data['names']['2']

ip=''
token=''

on='{"on":true}'
off='{"on":false}'

def flick(ip, token, light, state):
    r=requests.put('%s/api/%s/lights/%d/state' %(ip, token, light), data=state)
    print(r.text)

choice=input("%s or %s: " %(name1, name2))

if(choice[0:1]==name1[0:1]):
    ip=ip1
    token=token1
elif(choice[0:1]==name2[0:1]):
    ip=ip2
    token=token2
else: 
    print("invalid name.")
    exit()

r=requests.get('%s/api/%s/lights/' %(ip, token))
lights=json.loads(r.text).keys()

for x in lights:
    flick(ip, token, int(x), on)
    time.sleep(1)
    flick(ip, token, int(x), off)
    time.sleep(1)
