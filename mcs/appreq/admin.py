from django.contrib import admin
from appreq.models import *
from tastypie.models import ApiKey, ApiAccess
# Register your models here.

from django.contrib import admin
admin.site.register(Mineral)
admin.site.register(CodeMaster)
admin.site.register(CodeDetail)

from django.contrib.sites.models import Site
from django.contrib.auth.models import *

# need site to access the admin
# admin.site.unregister(Site)
# need ApiAccess for accessing the admin
# admin.site.unregister(ApiAccess)
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(ApiKey)
