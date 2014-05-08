from tastypie.resources import ModelResource
from survey.models import Survey
from appreq.exceptions import CustomBadRequest
from tastypie.authentication import Authentication, MultiAuthentication
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.validation import Validation
from tastypie.exceptions import Unauthorized, TastypieError
from django.utils.timezone import now

from config import settings
# error handling imports
from tastypie import http, fields

from appreq.messages import Messages
import logging
logger = logging.getLogger(__name__)

def raise_error(msg):
    raise CustomBadRequest(msg=msg)

class CustomValidation(Validation):
    pass

class SurveyResource(ModelResource):

    class Meta:
        allowed_methods = ['get', 'post']
        always_return_data = True
        queryset = Survey.objects.all()
        authorization = Authorization()
        resource_name = 'survey'

    def hydrate(self, bundle):
        print 'hydrate Coordinates'#, bundle.data
        return bundle

    def _handle_500(self, request, exception):
        # if isinstance(exception, TastypieError):
        #     data = {
        #         'error_message': 
        #         getattr(settings, 'TASTYPIE_CANNED_ERROR', 'Sorry, this request could not be processed.'),
        #     }
        #     return self.error_response(request, data, response_class=http.HttpApplicationError)
        # else:
        #     return super(RequestResource, self)._handle_500(request, exception)

        # return super(RequestResource, self)._handle_500(request, exception.message)
        return self.error_response(request, {"error": exception}, response_class=http.HttpApplicationError)
 
    def obj_create(self, bundle, **kwargs):
        print 'obj_create'#, bundle.data
        return super(SurveyResource, self).obj_create(bundle, **kwargs)

    def hydrate(self, bundle):
        print 'hydrate', bundle.data
        if bundle and bundle.data:
            bundle.data['survey_date'] = now()
        return bundle

    def dehydrate(self, bundle):
        print "dehydrate"
        return bundle
