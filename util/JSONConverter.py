from flask import json

class JSONConverter:

    def _asdict(self, data):
        """Convert Suds object into serializable format"""
        result = {}

        for key, value in dict(data).iteritems():
            if hasattr(value, '__keylist__'):            
                result[key] = self._asdict(value)
            elif isinstance(value, list):
                # parse the list
                result[key] = []
                for item in value:
                    if hasattr(item, '__keylist__'):
                        result[key].append(self._asdict(item))
                    else:
                        result[key].append(item)
            else:
                result[key] = value
        return result

    def suds_to_json(self, data):
        """ convert a suds object to a json object"""
        try:
            result = json.dumps(self._asdict(data))
        except Exception as e:            
            result = 'ERROR: {0}'.format(e)            
        return result
    
    
