![huelightsimage](https://i.imgur.com/pJNZcSE.png)

# huelights
A simple python script built to interact with Philips Hue lights in various ways.

To use this script, a json file is required, titled "lightsdata.json". Below is an example.
The API library "requests" is also required, which can be installed with:

```
>>> pip install requests
```

*lightsdata.json:*
```
{

    "names": {
    
        "1":"bob",
	
	"2": "mike"
	      
    },
    
    "tokens": {
    
        "1": "tokentokentoken",
	
        "2": "tokentokentoken"
    
    },
    
    "ips": {
    
    	"1": "192.168.1.1",
        
	"2": "192.168.1.1"
    
    }

}
