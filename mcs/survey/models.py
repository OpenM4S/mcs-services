from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.
class Survey(models.Model):
	# FK
	application_id = models.IntegerField(_("application_id"), null=False)
	survey_no = models.CharField(_("survey_no"), max_length=20, null=False)
	# FK
	availibility = models.IntegerField(_("availibility"), null=False)
	# FK
	overlapping = models.IntegerField(_("overlapping"), null=False)
	survey_date = models.DateTimeField(_("survey_date"), null=False)
	# FK
	traced_by = models.IntegerField(_("traced_by"), null=False)
	# FK
	prepared_by = models.IntegerField(_("prepared_by"), null=False)
	# FK
	approved_by = models.IntegerField(_("approved_by"), null=False)
	survey_remarks = models.CharField(_("survey_remarks"), max_length=900, null=False)

	class Meta:
		verbose_name = "Survey"
