from django.contrib import admin
from django.utils.safestring import mark_safe
from django.conf import settings

from .models import Donation

class DonationAdmin(admin.ModelAdmin):
	exclude = ('image_path', 'charge')
	list_display = ('token', 'customer', 'date_created')
	readonly_fields = ('image_path_readonly', 'amount_charged')

	def image_path_readonly(self, instance):
		return mark_safe('<img width=400 src="{0}{1}"><br><a href="{0}{1}">Download</a>'.format(settings.MEDIA_URL, instance.image_path))

	image_path_readonly.short_description = "Image uploaded by user"

	def amount_charged(self, instance):
		return '${0}'.format(instance.charge.amount)

admin.site.register(Donation, DonationAdmin)