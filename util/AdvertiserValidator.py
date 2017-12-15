
from dfpServices.auth import *
import logging

log = logging.getLogger('AdvertiserValidator')

class AdvertiserValidator:
    
    
    
    def validate(self,advertiserId):
          
        dfp_client = getDFPClient()
        company_service = dfp_client.GetService('CompanyService', version='v201705')
        query = 'WHERE id = :id '
        values = [
            {'key': 'id',
            'value': {
                  'xsi_type': 'TextValue',
               'value': advertiserId
           }},
        ]
          # Create a statement to select companies.
        statement = dfp.FilterStatement(query, values)
        
          # Retrieve a small amount of companies at a time, paging
          # through until all companies have been retrieved.
         
        while True:
            response = company_service.getCompaniesByStatement(statement.ToStatement())
            if 'results' in response:
                for company in response['results']:
                    # Print out some information for each company.
                    log.info('Company with ID "%d", name "%s", and type "%s" was found.\n' %
                          (company['id'], company['name'], company['type']))
                    statement.offset += dfp.SUGGESTED_PAGE_LIMIT
            else:
                break
        found = response['totalResultSetSize']
        log.info("AdvertiserValidator ,found "+ str(found))
        
        return found