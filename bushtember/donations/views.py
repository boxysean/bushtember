from django.shortcuts import render, render_to_response
from django.conf import settings

import payments
import payments.forms
print dir(payments.forms)
from payments.forms import DonateForm


def demo_view(request):
	form = DonateForm()

	return render_to_response('demo.html', {
		'form': form,
		'settings': settings,
	})

def demo_upload_view(request):
	return render_to_response('demo_upload.html', {
		'settings': settings,
	})	