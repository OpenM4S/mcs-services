from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

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
    license_type = models.IntegerField(_("license_type_id"), null=False)
    # FK
    mineral_type = models.IntegerField(_("mineral_type_id"), null=False)
    # FK
    total_area = models.IntegerField(_("total_area"), null=False)
    # FK
    unit_type = models.IntegerField(_("unit_type_id"), null=False)
    # FK
    topo_sheet = models.IntegerField(_("topo_sheet_no"), max_length=100, null=False)
    # FK
    request_status = models.IntegerField(_("request_status"), null=False)
    request_status_date = models.DateTimeField(_("request_status_date"), null=False)
    request_status_remarks = models.CharField(_("request_status_remarks"), max_length=900, null=True)

    class Meta:
        verbose_name = "Application Request"

class Coordinate(models.Model):
    request = models.ForeignKey(Request, related_name='coordinates')
    request_coord_no = models.CharField(_("request_coordinates_no"), max_length=20, null=False)
    latitude = models.DecimalField(_("latitude"), max_digits=8, decimal_places=5, null=False)
    longitude = models.DecimalField(_("longitude"), max_digits=8, decimal_places=5, null=False)
    elevation = models.DecimalField(_("elevation"), max_digits=15, decimal_places=5, null=True)

    class Meta:
        verbose_name = "coordinates"

class CodeMaster(models.Model):
    # cm_id
    name  = models.CharField(_("name"), max_length=30, null=False)
    display_name = models.CharField(_("display_name"), max_length=50, null=False)
    description = models.CharField(_("description"), max_length=900, null=False)
    # islocked
    # isactive

class CodeDetail(models.Model):
    # Code_Id
    cm_id = models.ForeignKey(CodeMaster, related_name='codedetails')
    name  = models.CharField(_("name"), max_length=30, null=False)
    display_name = models.CharField(_("display_name"), max_length=50, null=False)
    short_name = models.CharField(_("short_name"), max_length=30, null=False)
    description = models.CharField(_("description"), max_length=900, null=False)
    sequence_no = models.IntegerField(_("sequence_no"), null=False)
    value = models.IntegerField(_("value"), null=False)
    range_from = models.IntegerField(_("range_from"), null=False)
    range_to = models.IntegerField(_("range_to"), null=False)
    # is_default
    # is_active
    # color

class Mineral(models.Model):
    # mineral_id
    # mineral_no
    mineral_name = models.CharField(_("mineral_name"), max_length=30, null=False)
    chemical_formula = models.CharField(_("formula"), max_length=200, null=False)
    description = models.CharField(_("description"), max_length=900, null=False)
    mineral_category = models.ForeignKey(CodeDetail, related_name='minerals1')
    mineral_type = models.ForeignKey(CodeDetail, related_name='minerals2')
    rock_category = models.ForeignKey(CodeDetail, related_name='minerals3')
    rock_type = models.ForeignKey(CodeDetail, related_name='minerals4')
    mineral_unit = models.ForeignKey(CodeDetail, related_name='minerals5')
    group = models.ForeignKey(CodeDetail, related_name='minerals')
    # image
    # isactive
