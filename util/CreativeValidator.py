from dfpServices.get_creative_template import *
from dfpServices.auth import *
from util.JSONConverter import *

class CreativeValidator:
    
    def validate(self,creative):
        templateId = creative['creativeTemplateId']
        
        dfp_client = getDFPClient()
        
        creative_template = getDFPCreativeTemplate(dfp_client,templateId)
        
        encoder = JSONConverter()
    
        creative_template_json = encoder.suds_to_json(creative_template)
  
        the_dict = json.loads(creative_template_json)
 # print(creative_template_json)
        mandatory_fields = ['creativeTemplateId', 'name', 'advertiserId', 'creativeTemplateVariableValues', 'size', 'destinationUrl']
  
        missing_fields=[]
        for va in the_dict["variables"]:
            if(va['isRequired'] == True):
                mandatory_fields.append(va['uniqueName']) 
                
        creative_fields = creative.keys()
  
        if 'creativeTemplateVariableValues' in creative_fields : 
            for v in creative['creativeTemplateVariableValues']:
                creative_fields.append(v['uniqueName'])
        
        for k in mandatory_fields:
            if(k in creative_fields):
                pass
       
            else :
                missing_fields.append(k)
                
        return missing_fields