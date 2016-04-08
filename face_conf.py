import time 
import requests
import cv2
import operator
import numpy as np

# Import library to display results
import matplotlib.pyplot as plt
%matplotlib inline 
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
# Display images within Jupyter

_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_key = "f48684512c624aaeb3d3fadff6f5f006" #Here you have to paste your primary key
_maxNumRetries = 10

urlImage = 'https://scontent-hkg3-1.xx.fbcdn.net/hphotos-xfa1/v/t1.0-9/12418057_1129064750460767_2377002256503624139_n.jpg?oh=2c81f2c9c189a049dc5d55bae6337458&oe=57BF338D'

# Emotion parameters
params = { } 

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/json' 

json = { 'url': urlImage } 

retries = 0
result = None

while True:
 
    response = requests.request( 'post', _url,json=json,data = None,headers = headers,params = params )

    if response.status_code == 429: 
        
        print "Message: %s" % ( response.json()['error']['message'] )
        
        if retries <= _maxNumRetries: 
            time.sleep(1) 
            retries += 1
            continue
        else: 
            print 'Error: failed after retrying!'
            break

    elif response.status_code == 200 or response.status_code == 201:
        if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
            result = None 
        elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
            if 'application/json' in response.headers['content-type'].lower(): 
                result = response.json() if response.content else None 
            elif 'image' in response.headers['content-type'].lower(): 
                result = response.content
    else:
        print "Error code: %d" % ( response.status_code )
        print "Message: %s" % ( response.json()['error']['message'] )
        
    break
print result
