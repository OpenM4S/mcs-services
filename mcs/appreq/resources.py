from tastypie.resources import ModelResource
from appreq.models import Request, Coordinate
from appreq.exceptions import CustomBadRequest
from tastypie.authentication import Authentication, MultiAuthentication
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.validation import Validation
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from django.utils.timezone import now

from config import settings
# error handling imports
from tastypie import http, fields
from tastypie.resources import ModelResource
from tastypie.exceptions import TastypieError

from messages import Messages
import logging
logger = logging.getLogger(__name__)

def raise_error(msg):
    # return {'success': False, 'message': msg or ''}
    raise CustomBadRequest(msg=msg)

class CustomValidation(Validation):

    fn_len, ln_length, cnic_len = 4, 4, 13
    required = ['request_no', 'first_name', 'last_name', 'license_type', 'mineral_type', 'total_area', 'phone', 'unit_type', 'topo_sheet', 'coordinates']
    unique = ['request_no']

    # TODO: validate empty strings, invalid integers, data types (can't put strings instead of integers) 
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return raise_error('Invalid data!')

        for key in self.required:
            if key not in bundle.data:
                return raise_error("%s is a required field!" %(''.join(x for x in key.title()).replace('_',"  "),))
            v = bundle.data[key]
            if isinstance(v, basestring) and  len(v) <= 0:
                return raise_error("%s must have a valid value!" %(''.join(x for x in key.title()).replace('_',"  "),))

        cnic = self.validate_cnic(bundle.data)
        print 'after', cnic
        if 'success' in cnic and not cnic['success']: return cnic

    def validate_cnic(self, data):
        cnic = data['cnic'] if 'cnic' in data else None
        print 'validate_cnic ', cnic
        if cnic is None or len(str(cnic)) != self.cnic_len:
            return raise_error('CNIC must be {l} characters with digits only!'.format(l=self.cnic_len))
        return {}


### Request Coordinate Resource -- Bottom
class CoordinateResource(ModelResource):
    request = fields.ToOneField('appreq.resources.RequestResource', 'request', null=True)

    class Meta:
        allowed_methods = ['get', 'post']
        always_return_data = True
        queryset = Coordinate.objects.all()
        authorization = Authorization()
        resource_name = 'coordinates'

    def hydrate(self, bundle):
        print 'hydrate Coordinates', bundle.data
        return bundle

### Request Resource -- Top
class RequestResource(ModelResource):
    coordinates = fields.ToManyField('appreq.resources.CoordinateResource', 'coordinates', full=True)

    class Meta:
        allowed_methods = ['get', 'post']
        always_return_data = True
        queryset = Request.objects.all()
        resource_name = 'requests'
        always_return_data = True
        field_list_to_remove = ['first_name', 'middle_name', 'last_name', 'email', 'location','phone', 'total_area', 'request_status_remarks', 'unit_type', 'topo_sheet']
        validation = CustomValidation()
        authorization = Authorization()

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
        print 'obj_create', bundle.data
        if bundle.data and 'coordinates' not in bundle.data:
            logger.error(Messages.no_coordinates)
            return raise_error(Messages.no_coordinates)
        return super(RequestResource, self).obj_create(bundle, **kwargs)

    def hydrate(self, bundle):
        if bundle and bundle.data:
            bundle.data['request_date'] = now()
            bundle.data['request_status'] = 0
            bundle.data['request_status_date'] = now()
            bundle.data['request_status_remarks'] = 'No comments!'
        return bundle

    def dehydrate(self, bundle):
        # print "dehydrate"
        f, m, l  = bundle.obj.first_name or '', bundle.obj.middle_name or '', bundle.obj.last_name or ''
        bundle.data['request_by'] = '%s %s %s' %(f, m, l)
        return bundle

    def alter_list_data_to_serialize(self, request, to_be_serialized):
        for obj in to_be_serialized['objects']:
            print obj.data
            for field_name in self._meta.field_list_to_remove:
                if field_name in obj.data: del obj.data[field_name]
        return to_be_serialized

###
class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")