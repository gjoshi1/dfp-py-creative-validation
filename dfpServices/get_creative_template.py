from googleads import dfp

def getDFPCreativeTemplate(client, creativeTemplate_id): 
    creative_template_service = client.GetService(
      'CreativeTemplateService', version='v201705')
    values = [
        {
      'key': 'id',
      'value': {
          'xsi_type': 'NumberValue',
          'value': creativeTemplate_id
      }
    }]
    query = 'WHERE id = :id'
    statement = dfp.FilterStatement(query, values, 1)
    
    
    # Get creatives by statement.
    response = creative_template_service.getCreativeTemplatesByStatement(
        statement.ToStatement())
    
    if 'results' in response:
    # Update each local creative object by changing its destination URL.
        creativesTemplates = []
        for creativeTemplate in response['results']:
            creativesTemplates.append(creativeTemplate)

    return creativesTemplates[0]
