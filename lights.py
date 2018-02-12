import time,sys,requests,json

try:
    data=json.load(open('lightsdata.json'))
except:
    print(RED+UNDERLINE+"\nCould not read lightsdata.json. Does it exist?"+END+"\n\n")
    exit()

ip=''
token=''
on='{"on":true}'
off='{"on":false}'

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, UNDERLINE, END = '\033[36;1m', '\033[91;1m', '\33[37;1m', '\33[93;1m', '\033[35;1m', '\033[32;1m', '\033[4m', '\033[0m'

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

sys.stdout.write(BLUE+UNDERLINE+"Choose a Hue Box:\n\n"+END)

for x in data['ips']:
    sys.stdout.write(YELLOW+"["+MAGENTA+x+YELLOW+"]: "+WHITE+data['ips'][x]+END+"\n")
print("\n")

try:
    choice=input(MAGENTA+">>> "+END)
    ip='https://'+data['ips']['%s' %choice]
    token=data['tokens']['%s' %choice]
except:
    print(RED+UNDERLINE+"\nInvalid choice."+END+"\n\n")
    exit()

r=requests.get('%s/api/%s/lights/' %(ip, token))
lights=json.loads(r.text).keys()

cycle()
