import os
import yaml
from googleads import dfp
from flask import json

dfp_client = None
isConfigSet = False

def getDFPClient():
    
    global isConfigSet
    if(isConfigSet == False):
         initConfig()
    global dfp_client
    if(dfp_client == None):
        dfp_client = dfp.DfpClient.LoadFromStorage()
        
    return dfp_client

def initConfig():
    print("INITIALIZING CONFIG...")
    fname = "/root/googleads.yaml"
    flask_env = os.environ['NODE_ENV']
    fnameenv = "config/googleads-"+flask_env+".yaml"
    
    stream = file(fnameenv, 'r') 
    newdct = yaml.load(stream)
    
    with open(fname, "w") as f:
       yaml.dump(newdct,f,default_flow_style=False)
       global isConfigSet
       isConfigSet = True
       

    