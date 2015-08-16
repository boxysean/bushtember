from django.shortcuts import render, render_to_response
from django.conf import settings

from payments.forms import DonationForm


def demo_view(request):
	form = DonationForm()

	return render_to_response('demo.html', {
		'form': form,
		'settings': settings,
	})

def demo_upload_view(request):
	return render_to_response('demo_upload.html', {
		'settings': settings,
	})	