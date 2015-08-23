from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.conf import settings

from payments.forms import DonateForm

from .models import UploadPhotoToken


def donate_view(request):
	form = DonateForm()

	return render_to_response('donations/donate.html', {
		'form': form,
		'settings': settings,
	})

def upload_photo_view(request, upload_token_value=None):
	if upload_token_value is None:
		return redirect(reverse(donate_view))

	upload_token = UploadPhotoToken.objects.filter(token=upload_token_value)

	if len(upload_token) == 0:
		return redirect(reverse(donate_view))

	upload_token = upload_token.first()

	customer = upload_token.customer
	print customer

	print upload_token.charge.amount

	return render_to_response('donations/upload_photo.html', {
		'settings': settings,
		'upload_token': upload_token,
		'customer': customer
	})