from uuid import uuid4
from django.conf import settings

from django.db import models

from payments.models import Customer, Charge

def generate_token():
	return uuid4().hex

class Donation(models.Model):
	date_created = models.DateTimeField(auto_now_add=True)
	token = models.CharField(max_length=36, null=False, default=generate_token, db_index=True)
	customer = models.ForeignKey(Customer)
	charge = models.ForeignKey(Charge)
	uploaded_image = models.ImageField(null=True, blank=True, upload_to='uploads')
	uploaded_image_approved = models.NullBooleanField(null=True)
	modified_image = models.ImageField(null=True, blank=True, upload_to='uploads')
	modified_image_approved = models.NullBooleanField(null=True)
	collage_image = models.ImageField(null=True, blank=True, upload_to='uploads')

	def __unicode__(self):
		return u'<Donation ({0}, ${1})>'.format(self.customer.name, self.charge.amount)
