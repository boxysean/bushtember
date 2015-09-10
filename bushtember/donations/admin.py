from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings

from .models import Donation

class DonationAdmin(admin.ModelAdmin):
	exclude = ('uploaded_image', 'charge')
	list_display = ('token', 'customer', 'date_created')
	readonly_fields = ('uploaded_image_readonly', 'amount_charged', 'email')

	def uploaded_image_readonly(self, instance):
		uploaded_image = instance.uploaded_image.name.split('/')[-1]
		return mark_safe('<img width=400 src="{0}{1}"><br><a href="{0}{1}">Download</a>'.format(settings.MEDIA_URL + "uploads/", uploaded_image))

	uploaded_image_readonly.short_description = "Image uploaded by user"

	def amount_charged(self, instance):
		return '${0}'.format(instance.charge.amount)

	def email(self, instance):
		return '{0}'.format(instance.customer.email)

admin.site.register(Donation, DonationAdmin)