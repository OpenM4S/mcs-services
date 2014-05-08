import json
from tastypie.exceptions import TastypieError
from tastypie.http import HttpBadRequest

class CustomBadRequest(TastypieError):

    def __init__(self, code='', msg=''):
        self.response = {'success': False, 'code': code or 'unknown', 'message': msg or 'An error occurred!'}

    @property
    def response(self):
        return HttpBadRequest(json.dumps(self._response), content_type='application/json')

    @response.setter
    def response(self, value):
        self._response = value
    
