from django.shortcuts import render, render_to_response
from django.conf import settings

from payments.forms import PlanForm


def demo_view(request):
	form = PlanForm()

	return render_to_response('demo.html', {
		'form': form,
		'settings': settings
	})