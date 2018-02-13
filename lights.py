import time,sys,requests,json,random

ip, token='', ''
on, off='{"on":true}', '{"on":false}'
functions=["cycle","rainbow"]

def response():
    return input(MAGENTA+"\n>>> "+END)

def choiceError():
    print(RED+UNDERLINE+"\nInvalid choice."+END+"\n\n")
    exit()

def apiError():
    print(RED+UNDERLINE+"\nCould not access API of selected bridge."+END+"\n\n")
    exit()

def flick(ip, token, light, lightData):
    r=requests.put('%s/api/%s/lights/%d/state' %(ip, token, light), data=lightData)
    print(r.text)

def cycle(n):
    for i in range(n):
        for x in lights:
            flick(ip, token, int(x), on)
            time.sleep(1)
            flick(ip, token, int(x), off)
            time.sleep(1)

def rainbow(n):
    for i in range(n):
        for x in lights:
            flick(ip, token, int(x), '{"xy": [%0.4f, %0.4f]' %(random.uniform(0,1), random.uniform(0,1))+"}")
            time.sleep(1)


try:
    data=json.load(open('lightsdata.json'))
except:
    print(RED+UNDERLINE+"\nCould not read lightsdata.json. Does it exist?"+END+"\n\n")
    exit()

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

sys.stdout.write(BLUE+UNDERLINE+"Choose a Hue Bridge:\n\n"+END)

for x in data['ips']:
    sys.stdout.write(YELLOW+"["+MAGENTA+x+YELLOW+"]: "+WHITE+data['ips'][x]+END+"\n")

try:
    ipChoice=response()
    ip='http://'+data['ips'][str(ipChoice)]
    token=data['tokens'][str(ipChoice)]
except:
    choiceError()

sys.stdout.write(BLUE+UNDERLINE+"\n\nChoose a function:\n\n"+END)

for x in range(0, len(functions)):
    sys.stdout.write(YELLOW+"["+MAGENTA+str(x+1)+YELLOW+"]: "+WHITE+functions[x].capitalize()+END+"\n")

try:
    funcChoice=int(response())
except:
    choiceError()

sys.stdout.write(BLUE+UNDERLINE+"\n\nHow many repeats?\n"+END)

try:
    repeats=int(response())
except:
    choiceError()

try:
    r=requests.get('%s/api/%s/lights/' %(ip, token))
except:
    apiError()

lights=json.loads(r.text).keys()

if funcChoice is 1:
    cycle(repeats)
if funcChoice is 2:
    rainbow(repeats)