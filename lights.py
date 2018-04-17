import sys, requests, json, random, bridges
from time import sleep

#Since the handler is modular, they must identical to the function that they refer to
functions=['on', 'off', 'color', 'cycle', 'rainbow']

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
BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, UNDERLINE, END = '\33[36;1m', '\33[91;1m', '\33[37;1m', '\33[93;1m', '\33[35;1m', '\33[32;1m', '\33[4m', '\033[0m'

def apiError():
    sys.stdout.write(RED+UNDERLINE+"\n\nCould not access API of selected bridge."+END+"\n\n")
    sys.exit()

def choiceError():
    sys.stdout.write(RED+UNDERLINE+"\nInvalid choice."+END+"\n\n\n")
    bridgeHandler()

def unknownError():
    sys.stdout.write(RED+UNDERLINE+"\n\nAn Error Occurred."+END+"\n\n")
    sys.exit()

#Get user's choice in an integer
def intResponse():
    try:
        return int(input(MAGENTA+"\n>>> "+END))
    except KeyboardInterrupt:
        print("\n")
        sys.exit()
    except:
        choiceError()

#Change state of light
def flick(ip, token, light, lightData):
    try:
        r=requests.put('http://%s/api/%s/lights/%d/state' %(ip, token, light), data=lightData)
    except:
        apiError()

#Turn all lights on
def on(ip, token, lights):
    for x in lights:
        flick(ip, token, int(x), ON)

    funcHandler(ip, token, lights)

#Turn all lights off
def off(ip, token, lights):
    for x in lights:
        flick(ip, token, int(x), OFF)

    funcHandler(ip, token, lights)

#Cycle through every light and turn it on and off
def cycle(ip, token, lights):
    n=repeatHandler()

    for i in range(n):
        for x in lights:
            try:
                flick(ip, token, int(x), ON)
                sleep(1)
                flick(ip, token, int(x), OFF)
                sleep(1)
            except KeyboardInterrupt:
                print("\n")
                sys.exit()
            except:
                unknownError()

    funcHandler(ip, token, lights)

#Cycle through all lights and change the color
def rainbow(ip, token, lights):
    n=repeatHandler()

    for i in range(n):
        for x in lights:
            try:
                flick(ip, token, int(x), '{"xy": [%0.4f, %0.4f]' %(random.uniform(0,1), random.uniform(0,1))+"}")
                sleep(1)
            except KeyboardInterrupt:
                print("\n")
                sys.exit()
            except:
                unknownError()

    funcHandler(ip, token, lights)

#Change the color of the lights
def color(ip, token, lights):
    c=colorHandler()

    try:
        for x in lights:
            flick(ip, token, int(x), c)
    except:
        choiceError()
    
    funcHandler(ip, token, lights)

#Get new token
def generateToken(ip):
    sys.stdout.write(YELLOW+"\n\nNo token detected; generating a new one.\n\n\n"+END)

    try:
        sleep(1)
    except KeyboardInterrupt:
        print("\n")
        sys.exit()
    except:
        unknownError()

    #Wait up to 5 minutes for link button to be pressed
    i=0
    try:
        while i<=600:
            sys.stdout.write(BLUE+UNDERLINE+"\rPlease press link button on the bridge"+('.'*(i%3+1))+END)
            sys.stdout.flush()

            token=bridges.getToken(ip)

            if token is not '':
                return token

            sleep(0.5)
            i=i+1
    except KeyboardInterrupt:
        print("\n")
        sys.exit()
    except:
        unknownError()
    
    #If it reaches here, we assume token generation failed
    sys.stdout.write(RED+UNDERLINE+"\n\n\nCould not generate token."+END+"\n\n")
    sys.exit()

#Ask for color choice and then store input
def colorHandler():
    sys.stdout.write(BLUE+UNDERLINE+"\n\nWhich color?\n\n"+END)
    
    #Enumerate through the color values and store the color data in a new array
    #We have to do this because Python dictionaries aren't indexed, and I am not importing collections
    tempColors=[]
    for c, color in enumerate(lColors):
        sys.stdout.write(YELLOW+"["+MAGENTA+str(c+1)+YELLOW+"]: "+WHITE+color.capitalize()+END+"\n")
        tempColors.append(lColors[color])

    return tempColors[intResponse()-1]

#Ask for amount of repeats then store input
def repeatHandler():
    sys.stdout.write(BLUE+UNDERLINE+"\n\nHow many repeats?\n"+END)

    return intResponse()

#Function selector
def funcHandler(ip, token, lights):
    sys.stdout.write(BLUE+UNDERLINE+"\n\nChoose a function:\n\n"+END)

    #List all functions
    for x in range(0, len(functions)):
        sys.stdout.write(YELLOW+"["+MAGENTA+str(x+1)+YELLOW+"]: "+WHITE+functions[x].capitalize()+END+"\n")

    funcChoice=intResponse()

    if funcChoice<1 or funcChoice>len(functions):
        choiceError()

    #Call cooresponding function
    eval(functions[funcChoice-1]+'(ip, token, lights)')

#Token and ip selector
def bridgeHandler():
    sys.stdout.write(BLUE+UNDERLINE+"Choose a Hue Bridge:\n\n"+END)

    ips = bridges.scan()

    #List all gathered ips
    for x in ips:
        sys.stdout.write(YELLOW+"["+MAGENTA+str((ips.index(x)+1))+YELLOW+"]: "+WHITE+x+END+"\n")

    ipChoice=intResponse()

    if ipChoice<1 or ipChoice>len(ips):
        choiceError()

    #Set chosen ip and token
    ip=ips[ipChoice-1]
    if ip not in data:
        token=generateToken(ip)
        data[ip]=token
        with open('lightsdata.json', 'w') as f:
            json.dump(data, f)
    else:
        token=data[ip]

    #Test API, and gather all available lights
    try:
        r=requests.get('http://%s/api/%s/lights/' %(ip, token))
        lights=json.loads(r.text).keys()
    except:
        apiError()

    funcHandler(ip, token, lights)

try:
    data=json.load(open('lightsdata.json'))
except:
    sys.stdout.write(RED+UNDERLINE+"\nCould not read lightsdata.json. Does it exist?"+END+"\n\n")
    exit()

#Welcome message
sys.stdout.write("\n\n\n"+BLUE+WHITE+
                 " -------------------------------------------\n"+
                 WHITE+"| "+MAGENTA+"█░░█ "+BLUE+"█░░█ "+GREEN+"█▀▀ "+MAGENTA+"█░░ "+BLUE+"░▀░ "+GREEN+"█▀▀▀ "+MAGENTA+"█░░█ "+BLUE+"▀▀█▀▀ "+GREEN+"█▀▀"+WHITE+" |\n"+
                 WHITE+"| "+MAGENTA+"█▀▀█ "+BLUE+"█░░█ "+GREEN+"█▀▀ "+MAGENTA+"█░░ "+BLUE+"▀█▀ "+GREEN+"█░▀█ "+MAGENTA+"█▀▀█ "+BLUE+"░░█░░ "+GREEN+"▀▀█"+WHITE+" |\n"+ 
                 WHITE+"| "+MAGENTA+"▀░░▀ "+BLUE+"░▀▀▀ "+GREEN+"▀▀▀ "+MAGENTA+"▀▀▀ "+BLUE+"▀▀▀ "+GREEN+"▀▀▀▀ "+MAGENTA+"▀░░▀ "+BLUE+"░░▀░░ "+GREEN+"▀▀▀"+WHITE+" |  "+
                 WHITE+"v2.0\n"+
                 " -------------------------------------------\n"+
                 RED+"Made by: {}Collin Murch ({}@collinmurch{}){}".format(YELLOW, BLUE, YELLOW, END).center(80)+
                 "\n\n\n".center(0))

bridgeHandler()
