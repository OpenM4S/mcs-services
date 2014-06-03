from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

class CodeMaster(models.Model):
    # cm_id
    name  = models.CharField(_("name"), max_length=30, null=False)
    display_name = models.CharField(_("display_name"), max_length=50, null=False)
    description = models.CharField(_("description"), max_length=900, null=True)
    is_locked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.display_name

class CodeDetail(models.Model):
    # Code_Id
    code_master = models.ForeignKey(CodeMaster, related_name='details')
    name  = models.CharField(_("name"), max_length=30, null=False)
    display_name = models.CharField(_("display_name"), max_length=50, null=False)
    short_name = models.CharField(_("short_name"), max_length=30, null=True)
    description = models.CharField(_("description"), max_length=900, null=True)
    sequence_no = models.IntegerField(_("sequence_no"), null=True)
    value = models.IntegerField(_("value"), null=True)
    range_from = models.IntegerField(_("range_from"), null=True)
    range_to = models.IntegerField(_("range_to"), null=True)
    is_default =  models.BooleanField(default=False)
    is_active =  models.BooleanField(default=True)

    def __unicode__(self):
        return self.display_name

    def toJson(self):
        return {'id':self.id, 'name' : self.name}

class Mineral(models.Model):
    dictionary = {}
    # mineral_id
    mineral_no = models.IntegerField(_("mineral_no"), max_length=20, null=False)
    mineral_name = models.CharField(_("mineral_name"), max_length=30, null=False)
    chemical_formula = models.CharField(_("formula"), max_length=200, null=True)
    description = models.CharField(_("description"), max_length=900, null=True)
    mineral_category = models.IntegerField(_("mineral_category"), null=True) #models.ForeignKey(CodeDetail, related_name='mineral_category')
    mineral_type = models.IntegerField(_("mineral_type"), null=True) #models.ForeignKey(CodeDetail, related_name='mineral_mineral_type')
    mineral_unit = models.IntegerField(_("mineral_unit"), null=True) #models.ForeignKey(CodeDetail, related_name='mineral_mineral_unit')
    rock_category = models.IntegerField(_("rock_category"), null=True) #models.ForeignKey(CodeDetail, related_name='mineral_rock_category')
    rock_type = models.IntegerField(_("rock_type"), null=True) #models.ForeignKey(CodeDetail, related_name='mineral_rock_type')
    group = models.IntegerField(_("group"), null=True) #models.ForeignKey(CodeDetail, related_name='mineral_group')
    image = models.ImageField(upload_to='img/')
    process_duration = models.IntegerField(_("range_to"), null=False)
    expire_before = models.IntegerField(_("range_to"), null=False)
    is_active = models.BooleanField(default=True)
    is_transferable = models.BooleanField()
    is_extendable = models.BooleanField()

    def __unicode__(self):
        return self.mineral_name

class License(models.Model):
    # license_type_id
    name = models.CharField(_("name"), max_length=30, null=False)
    description = models.CharField(_("description"), max_length=900, null=False)
    short_name = models.CharField(_("short_name"), max_length=20, null=False)
    license_category_id = models.ForeignKey(CodeDetail, related_name='licenses_category')
    license_type_id = models.ForeignKey(CodeDetail, related_name='licenses_type')
    renewal_years = models.IntegerField(_("renewal_years"), null=False)
    duration = models.IntegerField(_("duration"), null=False)
    maximum_renewal = models.IntegerField(_("maximum_renewal"), null=False)
    parent_id = models.IntegerField(_("parent_id"), null=False)
    process_duration = models.IntegerField(_("process_duration"), null=False)
    expire_before = models.IntegerField(_("expire_before"), null=False)
    is_transferable = models.BooleanField()
    is_extendable = models.BooleanField()

    def __unicode__(self):
        return self.name

class Request(models.Model):
    request_no = models.CharField(_("request_no"), max_length=10, null=False, blank=False, unique=True)
    first_name = models.CharField(_("request_first_name"), max_length=30, blank=False, null=False)
    middle_name = models.CharField(_("request_middle_name"), max_length=30, null=True)
    last_name = models.CharField(_("request_last_name"), max_length=30, null=False)
    cnic = models.CharField(_("request_cnic"), null=False, blank=False, max_length=15)
    email = models.EmailField(_("request_email"), null=True, max_length=254)
    phone = models.CharField(_("request_phone"), null=True, max_length=20)
    request_date = models.DateTimeField(_("request_date"), null=False, auto_now=True)
    # FK
    # license_type = models.ForeignKey(CodeDetail, related_name='request_license_type')
    # FK
    mineral_id = models.IntegerField(_("mineral_id"), null=False)#models.ForeignKey(CodeDetail, related_name='request_mineral_type')
    # FK
    total_area = models.IntegerField(_("total_area"), null=False)
    # FK
    topo_sheet = models.IntegerField(_("topo_sheet"), null=False)
    # FK
    request_status = models.IntegerField(_("request_status"), null=False)
    request_status_date = models.DateTimeField(_("request_status_date"), null=False)
    request_status_remarks = models.CharField(_("request_status_remarks"), max_length=900, null=True)

    class Meta:
        verbose_name = "Application Request"

    def __unicode__(self):
        return "Request by {fn} {ln}".format(fn=self.first_name,ln=self.last_name)

class Coordinate(models.Model):
    request = models.ForeignKey(Request, related_name='coordinates')
    request_coord_no = models.CharField(_("request_coordinates_no"), max_length=20, null=False)
    latitude = models.DecimalField(_("latitude"), max_digits=8, decimal_places=5, null=False)
    longitude = models.DecimalField(_("longitude"), max_digits=8, decimal_places=5, null=False)
    elevation = models.DecimalField(_("elevation"), max_digits=15, decimal_places=5, null=True)

    class Meta:
        verbose_name = "coordinates"

    def __unicode__(self):
        return "Latitude: {lat}, Longitude: {lon}".format(lat=self.latitude,lon=self.longitude)
