from tastypie.resources import ModelResource
from appreq.models import RequestModel
from tastypie.authentication import Authentication, MultiAuthentication
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.validation import Validation

class CustomValidation(Validation):

    required = ['request_no']
    unique = ['request_no']

    # TODO: validate empty strings, invalid integers, data types (can't put strings instead of integers) 
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return self.raise_error('Invalid data!')

        cnic = self.validate_cnic(bundle.data)
        if not cnic['success']: return cnic

        for key in self.required:
            v = bundle.data[key]
            if isinstance(v, basestring) and  len(v) <= 0:
                return self.raise_error("%s can't be empty" %(key,))

    def validate_cnic(self, data):
        cnic = data['cnic'] if 'cnic' in data else None
        if cnic is None:
            return self.raise_error('You must provide a valid CNIC!')

        if cnic and len(str(cnic)) != 15:
            return self.raise_error('CNIC must be 15 digits (No dashes)!')
        return {}

    def raise_error(self, msg):
        error = {'success': True, 'message': ''}
        error['success'] = False
        error['message'] = msg
        return error

class RequestResource(ModelResource):
    class Meta:
        allowed_methods = ['get', 'post']
        always_return_data = True
        queryset = RequestModel.objects.all()
        resource_name = 'appreq'
        always_return_data = True
        field_list_to_remove = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'location','phone', 'total_area', 'request_status_remarks', 'unit_type', 'topo_sheet']
        validation = CustomValidation()
        #excludes = ['id', 'email', 'location', 'topo_sheet']
        #fields = ['request_no', 'cnic', 'license_type', 'request_date', 'mineral_type', 'request_status']
        # authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()

    def dehydrate(self, bundle):
        print "dehydrate", bundle
        f, m, l  = bundle.obj.first_name, bundle.obj.middle_name, bundle.obj.last_name
        bundle.data['request_by'] = '%s %s %s' %(f if f else '', m if m else '', l if l else '')
        return bundle

    def alter_list_data_to_serialize(self, request, to_be_serialized):
        for obj in to_be_serialized['objects']:
            for field_name in self._meta.field_list_to_remove:
                del obj.data[field_name]
        return to_be_serialized



from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


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