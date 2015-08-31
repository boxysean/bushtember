from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.signals import request_finished
from django.db.models import signals
from django.template import RequestContext

from payments.forms import DonateForm
from .forms import ImageUploadForm

from .models import Donation


def test_view(request):
	return render_to_response('donations/base.html', {
		'settings': settings,
	})

def donate_view(request):
	form = DonateForm()

	return render_to_response('donations/donate.html', {
		'form': form,
		'settings': settings,
	})

def upload_photo_view(request, donation_token=None):
	if donation_token is None:
		return redirect(reverse(donate_view))

	donation = Donation.objects.filter(token=donation_token).first()

	if donation is None:
		return redirect(reverse(donate_view))

	if request.method == 'POST':
		print request.POST
		print request.FILES

		form = ImageUploadForm(request.POST, request.FILES)

		if form.is_valid():
			image = form.cleaned_data['image']
			donation.uploaded_image = image
			donation.save()
			return redirect(upload_photo_view, donation_token=donation_token)
		else:
			logging.error(form.errors)
			return HttpResponse(status=500)


	customer = donation.customer
	form = ImageUploadForm()

	uploaded_image = donation.uploaded_image.name.split('/')[-1]

	return render_to_response('donations/upload_photo.html', {
		'settings': settings,
		'donation': donation,
		'customer': customer,
		'form': form,
		'uploaded_image': uploaded_image
	}, context_instance=RequestContext(request))

