#!flask/bin/python
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
import sys
import os
import logging
from suds import WebFault
from suds.client import Client

from dfpServices.auth import *
from dfpServices.create_native_creative import *
from util.JSONConverter import *
from util.CreativeValidator import *
from util.AdvertiserValidator import *
from werkzeug.wsgi import DispatcherMiddleware
from googleads import dfp
from flask import Flask, Response, current_app, json, request,jsonify
from werkzeug.exceptions import default_exceptions
from urllib2 import HTTPError


# from WAPOTemplateCreative import *
# from WAPOSize import *
# from CreativeTemplateVariable import *
# from Asset import *
import base64
import urllib2
import uuid



#app = Flask(__name__)

app = Flask(__name__)
logging.getLogger('suds.client').setLevel(logging.ERROR)
log=app.logger
log.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)
encoder = JSONConverter()



@app.route('/')
def index():
    return 'DFP FLASK API'

@app.route('/health')
def healthcheck():
    return 'Healthy!', 200

@app.route('/test', methods=['GET'])
def test():
    return 'FLASK API!', 200

@app.route('/getEnv', methods=['GET'])
def getEnv():
    log.info("GET ENV "+os.environ['NODE_ENV'] )
    return os.environ['NODE_ENV']

@app.route('/dfp-adserving/api/getCreative/<int:creative_id>', methods=['GET'])
def get_creative(creative_id):
    log.info("GET CREATIVE "+str(creative_id))
    
    dfp_client = getDFPClient()
    templatecreative=getDFPCreative(dfp_client,creative_id)
    
    
    if(templatecreative == -1):
        abort(404,"Creative Not Found")
#    
    
    
    templatecreative = encoder.suds_to_json(templatecreative)
    
    log.info("CREATIVE FOUND")
    
    return templatecreative,200

@app.route('/dfp-adserving/api/getTemplateVariables/<int:template_id>', methods=['GET'])
def get_creative_template_variables(template_id):
        
        log.info("get_creative_template_variables "+str(template_id))
       
        dfp_client = getDFPClient()
        
        creative_template = getDFPCreativeTemplate(dfp_client,template_id)
        
       
    
        variables = creative_template['variables']
         
        variablesWithType = []
        tvar={}
        for va in variables:
            varType = ""
            defaultVal = ""
            description = ""
            isTrackingUrl = ""
            
            #type is not available as an attribute in templateVariables.
            #we use the class name of the templateVariable determines the type and add it as attribute.
            #the returned suds object looks line this :
            #(StringCreativeTemplateVariable){
            #    label = "RawHTML"
            #    uniqueName = "RawHTML"
             #   isRequired = False
            #    }

            
            if(va.__class__.__name__ == "UrlCreativeTemplateVariable"):
                varType = "URL"
            if(va.__class__.__name__ == "AssetCreativeTemplateVariable"):
                varType = "FILE"
            if(va.__class__.__name__ == "StringCreativeTemplateVariable"):
                varType = "TEXT"
            if(va.__class__.__name__ == "LongCreativeTemplateVariableValue"):
                varType = "NUMBER"
            if(va.__class__.__name__ == "ListStringCreativeTemplateVariable"):
                varType = "LIST"
            
            if(hasattr(va,"defaultValue")) :
                defaultVal = va["defaultValue"]
            if(hasattr(va,"description")) :
                description = va["description"]
            if(hasattr(va,"isTrackingUrl")) :
                isTrackingUrl = va["isTrackingUrl"]
                
            log.info(va)
            #Only the type URL has attribute isTrackingUrl
            if(varType == "URL") :
                tvar = {'label':va["label"],
                  'uniqueName':va["uniqueName"],
                  'isRequired':va["isRequired"],
                  'type' :varType,
                  'defaultValue':defaultVal,
                  'description':description,
                  'isTrackingUrl':isTrackingUrl}
            else :  
                tvar={'label':va["label"],
                  'uniqueName':va["uniqueName"],
                  'isRequired':va["isRequired"],
                  'type' :varType,
                  'defaultValue':defaultVal,
                  'description':description
                  }
           
            
            
            variablesWithType.append(tvar)
        
                        
        creative_template_json = encoder.suds_to_json(creative_template)
        
        #creative_template_json["variables"] = variablesWithType
        

        return jsonify({'variables':variablesWithType}),200
    

@app.route('/dfp-adserving/api/addCreative', methods=['POST'])
def create_creative():
    log.info("ADD CREATIVE")
    if not request.json or not 'creativeTemplateId' in request.json:
        abort(400,"Missing Field [creativeTemplateId]")
    if not 'destinationUrl' in request.json or len(request.json['destinationUrl'])==0 :
        abort(400,"Missing Field [destinationUrl]")
        
    advertiserValidator = AdvertiserValidator()
    found = advertiserValidator.validate(request.json['advertiserId'])
    if(found == 0):
        abort(400,"AdvertiserID " +str(request.json['advertiserId'])+" Not Found")
    
    creativeValidator = CreativeValidator()    
    missing_fields = creativeValidator.validate(request.json)
    
    if(len(missing_fields) > 0):
        abort(400,"Missing Fields " + str(missing_fields))
    
    dfp_client = getDFPClient()
    
    ADVERTISER_ID=request.json['advertiserId']
    creative = {
        'creativeTemplateId': request.json['creativeTemplateId'],
        'advertiserId' : request.json['advertiserId'],
        'name' : request.json['name'],
        'destinationUrl' : request.json['destinationUrl'],
        'size' :request.json['size'],
        'creativeTemplateVariableValues':request.json['creativeTemplateVariableValues']
        
    }
    
    
    newCreative = createNativeCreativewapo(dfp_client, ADVERTISER_ID,creative)
    
    log.info("NEW CREATIVE ADDED SUCCESSFULLY "+encoder.suds_to_json(newCreative))
    
    return jsonify({'creativeId': newCreative['id']}), 201

@app.route('/dfp-adserving/api/updateCreative', methods=['POST'])
def update_creative():
    log.info("UPDATE CREATIVE ")
    if not request.json or not 'creativeTemplateId' in request.json:
        abort(400,"Missing Field [creativeTemplateId]")
    if not request.json or not 'id' in request.json:
        abort(400,"Missing Field [id]")
    if not 'destinationUrl' in request.json or len(request.json['destinationUrl'])==0 :
        abort(400,"Missing Field [destinationUrl]")
    
    log.info(request.json['id'])
    
    advertiserValidator = AdvertiserValidator()
    found = advertiserValidator.validate(request.json['advertiserId'])
    if(found == 0):
        abort(400,"AdvertiserID " +str(request.json['advertiserId'])+" Not Found")
    
    creativeValidator = CreativeValidator()    
    missing_fields = creativeValidator.validate(request.json)
    
    if(len(missing_fields) > 0):
        abort(400,"Missing Fields " + str(missing_fields))
    
    
    dfp_client = getDFPClient()
    
    ADVERTISER_ID=request.json['advertiserId']
    
    
    creative = {
        'id': request.json['id'],
        'creativeTemplateId': request.json['creativeTemplateId'],
        'advertiserId' : request.json['advertiserId'],
        'name' : request.json['name'],
        'destinationUrl' : request.json['destinationUrl'],
        'size' :request.json['size'],
        'creativeTemplateVariableValues':request.json['creativeTemplateVariableValues']
        
    }
    
    updateNativeCreativewapo(dfp_client, ADVERTISER_ID,creative)
    
    log.info("CREATIVE UPDATED SUCCESSFULLY ")
    
    return jsonify({'creative': creative}), 201



@app.errorhandler(404)
def not_found(error):
    log.error(error)
    log.error('Page not found: %s', (request.path))
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def input_error(error):
    log.error("400 :"+error.description)
    return make_response(jsonify({'error': error.description}), 400)

@app.errorhandler(URLError)
def URL_error(error):
    log.error("URL ERROR "+error.description)
    return make_response(jsonify({'error': error.description}), 400)

@app.errorhandler(HTTPError)
def http_error(error):
    log.error("HTTP ERROR PAGE RETURN")
    
    log.error(error.description)
    return make_response(jsonify({'Forbidden': error.description}), 403)

@app.errorhandler(WebFault)
def data_error(error):
     
     error_json = encoder.suds_to_json(error.fault)
     log.error("WEBFAULT :"+error_json)
     #log.info(error_json['faultstring'])
     return make_response(jsonify({'error': error_json}), 400)
 

 



if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=False, use_evalex=True, enable_threads=True)
