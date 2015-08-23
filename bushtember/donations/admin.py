from django.contrib import admin

from .models import UploadPhotoToken

class UploadPhotoTokenAdmin(admin.ModelAdmin):
	fields = ('customer', 'token')
	list_display = ('token', 'customer', 'date_created')

admin.site.register(UploadPhotoToken, UploadPhotoTokenAdmin)