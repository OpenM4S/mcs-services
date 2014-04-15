from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

class RequestCoordinates(models.Model):
    request_id = models.IntegerField(_("license_type_id"), null=False)
    request_coord_no = models.IntegerField(_("request_coordinates_no"), null=False)
    latitude = models.DecimalField(_("latitude"), max_digits=8, decimal_places=5, null=False)
    longitude = models.DecimalField(_("longitude"), max_digits=8, decimal_places=5, null=False)
    elevation = models.DecimalField(_("elevation"), max_digits=15, decimal_places=5, null=True)


class RequestModel(models.Model):
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
    location = models.IntegerField(_("location_id"), null=False)
    # FK
    request_status = models.IntegerField(_("request_status"), null=False)
    request_status_date = models.DateTimeField(_("request_status_date"), null=False)
    request_status_remarks = models.CharField(_("request_status_remarks"), max_length=900, null=True)
