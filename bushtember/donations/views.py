from django.shortcuts import render, render_to_response

from payments.forms import PlanForm


def checkout_view(request):
	form = PlanForm()

	return render_to_response('checkout.html', {
		'form': form
	})