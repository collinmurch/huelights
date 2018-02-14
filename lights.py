import time,sys,requests,json,random
#Under heavy development -- #import generatetoken as gToken

ip, token='', ''
functions=["on", "off", "change color", "cycle", "rainbow"]

#Default data
lColors={
    'white' : '{"xy": [0.3146, 0.3304]}',
    'red'   : '{"xy": [0.6817, 0.2936]}',
    'blue'  : '{"xy": [0.154, 0.0806]}',
    'yellow': '{"xy": [0.4657, 0.4779]}',
    'purple': '{"xy": [0.216, 0.1099]}',
    'green' : '{"xy": [0.2611, 0.6316]}',
    'orange': '{"xy": [0.5574, 0.409]}'
}

ON, OFF='{"on":true}', '{"on":false}'

#Text colors
BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, UNDERLINE, END = '\033[36;1m', '\033[91;1m', '\33[37;1m', '\33[93;1m', '\033[35;1m', '\033[32;1m', '\033[4m', '\033[0m'

def apiError():
    print(RED+UNDERLINE+"\n\nCould not access API of selected bridge."+END+"\n\n")
    exit()

def choiceError():
    print(RED+UNDERLINE+"\n\nInvalid choice."+END+"\n\n")
    exit()

#Get user's choice in an integer
def intResponse():
    try:
        return int(input(MAGENTA+"\n>>> "+END))
    except:
        choiceError()

#Change state of light
def flick(ip, token, light, lightData):
    try:
        r=requests.put('%s/api/%s/lights/%d/state' %(ip, token, light), data=lightData)
    except:
        apiError()

    print(r.text)

#Turn all lights on
def on():
    for x in lights:
        flick(ip, token, int(x), ON)

#Turn all lights off
def off():
    for x in lights:
        flick(ip, token, int(x), OFF)

#Cycle through every light and turn it on and off
def cycle(n):
    for i in range(n):
        for x in lights:
            flick(ip, token, int(x), ON)
            time.sleep(1)
            flick(ip, token, int(x), OFF)
            time.sleep(1)

#Cycle through all lights and change the color
def rainbow(n):
    for i in range(n):
        for x in lights:
            flick(ip, token, int(x), '{"xy": [%0.4f, %0.4f]' %(random.uniform(0,1), random.uniform(0,1))+"}")
            time.sleep(1)

#Change the color of the lights
def color():
    sys.stdout.write(BLUE+UNDERLINE+"\n\nWhich color?\n\n"+END)
    
    #Enumerate through the color values and store the color data in a new array
    #We have to do this because Python dictionaries aren't indexed, and I am not importing collections
    tempColors=[]
    for c, color in enumerate(lColors):
        sys.stdout.write(YELLOW+"["+MAGENTA+str(c+1)+YELLOW+"]: "+WHITE+color.capitalize()+END+"\n")
        tempColors.append(lColors[color])

    colorChoice=intResponse()-1
    try:
        for x in lights:
            flick(ip, token, int(x), tempColors[colorChoice])
    except:
        choiceError()

try:
    data=json.load(open('lightsdata.json'))
except:
    print(RED+UNDERLINE+"\nCould not read lightsdata.json. Does it exist?"+END+"\n\n")
    exit()

#Welcome message
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

#List all ips
for x in data['ips']:
    sys.stdout.write(YELLOW+"["+MAGENTA+x+YELLOW+"]: "+WHITE+data['ips'][x]+END+"\n")

ipChoice=intResponse()

#Set chosen ip and token
ip='http://'+data['ips'][str(ipChoice)]
token=data['tokens'][str(ipChoice)]


sys.stdout.write(BLUE+UNDERLINE+"\n\nChoose a function:\n\n"+END)

#List all functions
for x in range(0, len(functions)):
    sys.stdout.write(YELLOW+"["+MAGENTA+str(x+1)+YELLOW+"]: "+WHITE+functions[x].capitalize()+END+"\n")

funcChoice=intResponse()

#Test API, and gather all available lights
try:
    r=requests.get('%s/api/%s/lights/' %(ip, token))
    lights=json.loads(r.text).keys()
except:
    apiError()

#Function handler
if funcChoice is 1:
    on()
elif funcChoice is 2:
    off()
elif funcChoice is 3:
    color()
else:
    sys.stdout.write(BLUE+UNDERLINE+"\n\nHow many repeats?\n"+END)

    repeats=intResponse()

    if funcChoice is 4:
        cycle(repeats)
    if funcChoice is 5:
        rainbow(repeats)