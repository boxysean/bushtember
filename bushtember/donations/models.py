from uuid import uuid4

from django.db import models

from payments.models import Customer, Charge

def generate_token():
	return uuid4().hex

class UploadPhotoToken(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	token = models.CharField(max_length=36, null=False, default=generate_token)
	customer = models.ForeignKey(Customer)
	charge = models.ForeignKey(Charge)

	def __unicode__(self):
		return u'UploadPhotoToken <{0}>'.format(token)
