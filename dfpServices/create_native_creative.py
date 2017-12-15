#!/usr/bin/python
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This code example creates a new native creative for a given advertiser.

To determine which companies are advertisers, run get_advertisers.py.

The code in this example will use app data from the Google sample app
'Pie Noon':

https://play.google.com/store/apps/details?id=com.google.fpl.pie_noon&hl=en

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""

import base64
import urllib2
import uuid
from flask import abort
import logging

# Import appropriate modules from the client library.
from googleads import dfp
from suds import WebFault
from urllib2 import URLError
from urllib2 import HTTPError

log = logging.getLogger('create_native_creative')
  
def createNativeCreativewapo(client, advertiser_id, wapocreative):
    
  
  
  
  # Initialize appropriate service.
    creative_service = client.GetService('CreativeService', version='v201705')

  # Use the system defined native app install creative template.
  # creative_template_id = '10004400'

  
    creative_asset = {}
    blob = []
    temp = {}
  
    for ctvobj in wapocreative['creativeTemplateVariableValues']:
        
        filename = 'file%s.png' % uuid.uuid4()
        if(ctvobj['type'] == "FILE"):
            
            try:
                
                image_data = urllib2.urlopen(ctvobj['value']).read()
           
                image_data = base64.b64encode(image_data)
            except WebFault as detail:
                log.error("CAUGHT WebFault")
                log.error(detail)
            except HTTPError, e:
                log.error("CAUGHT HTTP ERROR")
                abort(e.code, "REASON : " + e.reason + ", CAUSED BY INVALID FIELD :" + ctvobj['uniqueName'] + ", INVALID URL  :" + ctvobj['value'])
            except URLError, e:
                log.error("CAUGHT URL ERROR")
                abort(400, "REASON : " + e.reason + "INVALID FIELD :" + ctvobj['uniqueName'] + ", INVALID URL  :" + ctvobj['value'])
            
          # assetObj = Asset(image_data,'file%s.png' % uuid.uuid4())
          # ctvobj.asset = assetObj
           # asset={'assetByteArray': "",'fileName': filename}
            creative_asset = {
                'fileName': filename,
                'assetByteArray':image_data
            }
            temp = {'xsi_type': 'AssetCreativeTemplateVariableValue',
             'uniqueName': ctvobj['uniqueName'],
             'asset': {
                 'assetByteArray': image_data,
                 'fileName': 'file%s.png' % uuid.uuid4()
             }}
           # tempVar = {'xsi_type': ctvobj.xsi_type,'uniqueName': ctvobj.uniqueName,'asset':creative_asset}
        if(ctvobj['type'] == "URL"):
                temp = {'xsi_type': "UrlCreativeTemplateVariableValue",
                        'uniqueName': ctvobj['uniqueName'],
                        'value': ctvobj['value']}
         
        if(ctvobj['type'] == "TEXT"):
                temp = {'xsi_type': "StringCreativeTemplateVariableValue",
                        'uniqueName': ctvobj['uniqueName'],
                        'value': ctvobj['value']}
                
        if(ctvobj['type'] == "NUMBER"):
                temp = {'xsi_type': "LongCreativeTemplateVariableValue",
                        'uniqueName': ctvobj['uniqueName'],
                        'value': ctvobj['value']}
         
        blob.append(temp)
     #END OF for 
    
   
        # Create creative from templates.
    creative = {
     'xsi_type': 'TemplateCreative',
     'name': wapocreative['name'],
     'advertiserId': advertiser_id,
     'size': wapocreative['size'],
     'creativeTemplateId': wapocreative['creativeTemplateId'],
     'destinationUrl': wapocreative['destinationUrl'],
     'creativeTemplateVariableValues': blob
     }
  # Call service to create the creative.

    creative = creative_service.createCreatives([creative])[0]

    # Display results.
    log.info ('Native creative with id \'%s\' and name \'%s\' was created'
         % (creative['id'], creative['name'].encode('utf-8').strip()))
    return creative


def updateNativeCreativewapo(client, advertiser_id, wapocreative):
    
  # Initialize appropriate service.
  creative_service = client.GetService('CreativeService', version='v201705')

  # Use the system defined native app install creative template.
  # creative_template_id = '10004400'

  
  creative_asset = {}
  blob = []
  temp = {}
  
  for ctvobj in wapocreative['creativeTemplateVariableValues']:
    #log.info(str(ctvobj['uniqueName']).encode('utf-8').strip())
    filename = 'file%s.png' % uuid.uuid4()
    if(ctvobj['type'] == "FILE"):
         #  log.info("BUILD ASSET")
        try:
            image_data = urllib2.urlopen(ctvobj['value']).read()
            image_data = base64.b64encode(image_data)
        except WebFault as detail:
            log.error("CAUGHT WEBFAULT")
            log.error(detail)
        except HTTPError, e:
            log.error("CAUGHT HTTP ERROR")
            
            abort(e.code, "REASON : " + e.reason + ", CAUSED BY INVALID FIELD :" + ctvobj['uniqueName'] + ", INVALID URL  :" + ctvobj['value'])
        except URLError, e:
            log.error("CAUGHT URL ERROR")
            abort(400, "REASON : " + e.reason + "INVALID FIELD :" + ctvobj['uniqueName'] + ", INVALID URL  :" + ctvobj['value'].encode('utf-8'))
          # assetObj = Asset(image_data,'file%s.png' % uuid.uuid4())
          # ctvobj.asset = assetObj
           # asset={'assetByteArray': "",'fileName': filename}
        creative_asset = {
       'fileName': filename,
       'assetByteArray':image_data
        }
        temp = {'xsi_type': 'AssetCreativeTemplateVariableValue',
             'uniqueName': ctvobj['uniqueName'],
             'asset': {
                 'assetByteArray': image_data,
                 'fileName': 'file%s.png' % uuid.uuid4()
        }}
           # tempVar = {'xsi_type': ctvobj.xsi_type,'uniqueName': ctvobj.uniqueName,'asset':creative_asset}
       
    if(ctvobj['type'] == "URL"):
           temp = {'xsi_type': "UrlCreativeTemplateVariableValue",
             'uniqueName': ctvobj['uniqueName'],
             'value': ctvobj['value']}
         
    if(ctvobj['type'] == "TEXT"):
           temp = {'xsi_type': "StringCreativeTemplateVariableValue",
             'uniqueName': ctvobj['uniqueName'],
             'value': ctvobj['value']}
    if(ctvobj['type'] == "NUMBER"):
                temp = {'xsi_type': "LongCreativeTemplateVariableValue",
                        'uniqueName': ctvobj['uniqueName'],
                        'value': ctvobj['value']}
         
    blob.append(temp)
      
    #End of for
   
# Create creative from templates.
  creative = {
     'xsi_type': 'TemplateCreative',
     'id': wapocreative['id'],
     'name': wapocreative['name'],
     'advertiserId': advertiser_id,
     'size': wapocreative['size'],
     'creativeTemplateId': wapocreative['creativeTemplateId'],
     'destinationUrl': wapocreative['destinationUrl'],
     'creativeTemplateVariableValues': blob
     }
  # Call service to create the creative.

  creative = creative_service.updateCreatives([creative])[0]

  
  # Display results.
  log.info ('Native creative with id \'%s\' and name \'%s\' was '
         'created '
         % (creative['id'], creative['name'].encode('utf-8')))
  
  
def getDFPCreative(client, creative_id): 
    creative_service = client.GetService('CreativeService', version='v201705')
    values = [
        {
      'key': 'id',
      'value': {
          'xsi_type': 'NumberValue',
          'value': creative_id
      }
    }]
    query = 'WHERE id = :id'
    statement = dfp.FilterStatement(query, values, 1)
    
    
    # Get creatives by statement.
    response = creative_service.getCreativesByStatement(
        statement.ToStatement())
    
    if 'results' in response:
    # Update each local creative object by changing its destination URL.
        creatives = []
        for creative in response['results']:
            creatives.append(creative)

    else:
        return -1
    
    return creatives[0]
