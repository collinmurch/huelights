import time,sys,requests,json

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

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\033[36;1m', '\033[91;1m', '\33[37;1m', '\33[93;1m', '\033[35;1m', '\033[32;1m', '\033[0m'

sys.stdout.write("\n\n\n"+BLUE+WHITE+
                 " -------------------------------------------\n"+
                 WHITE+"| "+MAGENTA+"█░░█ "+BLUE+"█░░█ "+GREEN+"█▀▀ "+MAGENTA+"█░░ "+BLUE+"░▀░ "+GREEN+"█▀▀▀ "+MAGENTA+"█░░█ "+BLUE+"▀▀█▀▀ "+GREEN+"█▀▀"+WHITE+" |\n"+
                 WHITE+"| "+MAGENTA+"█▀▀█ "+BLUE+"█░░█ "+GREEN+"█▀▀ "+MAGENTA+"█░░ "+BLUE+"▀█▀ "+GREEN+"█░▀█ "+MAGENTA+"█▀▀█ "+BLUE+"░░█░░ "+GREEN+"▀▀█"+WHITE+" |\n"+ 
                 WHITE+"| "+MAGENTA+"▀░░▀ "+BLUE+"░▀▀▀ "+GREEN+"▀▀▀ "+MAGENTA+"▀▀▀ "+BLUE+"▀▀▀ "+GREEN+"▀▀▀▀ "+MAGENTA+"▀░░▀ "+BLUE+"░░▀░░ "+GREEN+"▀▀▀"+WHITE+" |  "+
                 WHITE+"v1.0\n"+
                 " -------------------------------------------\n"+
                 RED+"Made by: {}Collin Murch ({}@collinmurch{}){}".format(YELLOW, BLUE, YELLOW, END).center(80)+
                 "\n\n\n".center(0))

def flick(ip, token, light, state):
    r=requests.put('%s/api/%s/lights/%d/state' %(ip, token, light), data=state)
    print(r.text)

def cycle():
    for x in lights:
        flick(ip, token, int(x), on)
        time.sleep(1)
        flick(ip, token, int(x), off)
        time.sleep(1)

choice=input("%s or %s: " %(name1, name2)).lower()

if(choice[0:1]==name1[0:1].lower()):
    ip=ip1
    token=token1
elif(choice[0:1]==name2[0:1].lower()):
    ip=ip2
    token=token2
else: 
    print("invalid name.")

r=requests.get('%s/api/%s/lights/' %(ip, token))
lights=json.loads(r.text).keys()

cycle()
