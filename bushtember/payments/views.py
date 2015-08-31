import json
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

import stripe

from . import settings as app_settings
from .forms import PlanForm, DonateForm
from .models import (
    Customer,
    CurrentSubscription,
    Event,
    EventProcessingException
)

from donations.models import Donation


class PaymentsContextMixin(object):

    def get_context_data(self, **kwargs):
        context = super(PaymentsContextMixin, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": app_settings.STRIPE_PUBLIC_KEY,
            "PLAN_CHOICES": app_settings.PLAN_CHOICES,
            "PAYMENT_PLANS": app_settings.PAYMENTS_PLANS
        })
        return context


def _ajax_response(request, template, **kwargs):
    response = {
        "html": render_to_string(
            template,
            RequestContext(request, kwargs)
        )
    }
    if "location" in kwargs:
        response.update({"location": kwargs["location"]})
    return HttpResponse(json.dumps(response), content_type="application/json")


class SubscribeView(PaymentsContextMixin, TemplateView):
    template_name = "payments/subscribe.html"

    def get_context_data(self, **kwargs):
        context = super(SubscribeView, self).get_context_data(**kwargs)
        context.update({
            "form": PlanForm
        })
        return context


class DonateView(PaymentsContextMixin, TemplateView):
    template_name = "donations/demo.html"

    def get_context_data(self, **kwargs):
        context = super(DonateView, self).get_context_data(**kwargs)
        context.update({
            "form": DonateForm
        })
        return context


class ChangeCardView(PaymentsContextMixin, TemplateView):
    template_name = "payments/change_card.html"


class CancelView(PaymentsContextMixin, TemplateView):
    template_name = "payments/cancel.html"


class ChangePlanView(SubscribeView):
    template_name = "payments/change_plan.html"


class HistoryView(PaymentsContextMixin, TemplateView):
    template_name = "payments/history.html"


@require_POST
@login_required
def change_card(request):
    try:
        customer = request.user.customer
        send_invoice = customer.card_fingerprint == ""
        customer.update_card(
            request.POST.get("stripe_token")
        )
        if send_invoice:
            customer.send_invoice()
        customer.retry_unpaid_invoices()
        data = {}
    except stripe.CardError as e:
        data = {"error": smart_str(e)}
    return _ajax_response(request, "payments/_change_card_form.html", **data)


@require_POST
@login_required
def change_plan(request):
    form = PlanForm(request.POST)
    try:
        current_plan = request.user.customer.current_subscription.plan
    except CurrentSubscription.DoesNotExist:
        current_plan = None
    if form.is_valid():
        try:
            request.user.customer.subscribe(form.cleaned_data["plan"])
            data = {
                "form": PlanForm(initial={"plan": form.cleaned_data["plan"]})
            }
        except stripe.StripeError as e:
            data = {
                "form": PlanForm(initial={"plan": current_plan}),
                "error": smart_str(e)
            }
    else:
        data = {
            "form": form
        }
    return _ajax_response(request, "payments/_change_plan_form.html", **data)


@require_POST
@login_required
def subscribe(request, form_class=PlanForm):
    data = {"plans": settings.PAYMENTS_PLANS}
    form = form_class(request.POST)
    if form.is_valid():
        try:
            try:
                customer = request.user.customer
            except ObjectDoesNotExist:
                customer = Customer.create(request.user)
            if request.POST.get("stripe_token"):
                customer.update_card(request.POST.get("stripe_token"))
            customer.subscribe(form.cleaned_data["plan"])
            data["form"] = form_class()
            data["location"] = reverse("payments_history")
        except stripe.StripeError as e:
            data["form"] = form
            data["error"] = smart_str(e) or "Unknown error"
    else:
        data["error"] = form.errors
        data["form"] = form
    return _ajax_response(request, "payments/_subscribe_form.html", **data)


@require_POST
@csrf_exempt
def donate(request, form_class=DonateForm):
    data = {}
    form = form_class(request.POST)

    stripe_token = request.POST.get('stripe_token')

    if not form.is_valid():
        logging.error('invalid donation form, but stripe was processed (stripe token = %s)' % (stripe_token))
    else:
        # record the data
        try:
            stripe_customer = stripe.Customer.create(source=stripe_token)

            customer, customer_created = Customer.objects.get_or_create(stripe_id=stripe_customer.stripe_id, defaults={
                'name': form.cleaned_data['name'],
                'address_city': stripe_customer.cards['data'][0]['address_city'],
                'address_country': stripe_customer.cards['data'][0]['address_country'],
                'address_line1': stripe_customer.cards['data'][0]['address_line1'],
                'address_line2': stripe_customer.cards['data'][0]['address_line2'],
                'address_state': stripe_customer.cards['data'][0]['address_state'],
                'address_zip': stripe_customer.cards['data'][0]['address_zip'],
                'email': stripe_customer.cards['data'][0]['name'],
            })

            charge = customer.charge(form.cleaned_data['amount'], send_receipt=False)

            donation = Donation(customer=customer, charge=charge)
            donation.save()

            charge.send_receipt()

            response = redirect(reverse('donations.views.upload_photo_view', kwargs={'donation_token': donation.token}))

            print 'RESPONSE'
            for key in dir(response):
                print key, getattr(response, key)

            print 'REQUEST'
            for key in dir(response):
                print key, getattr(response, key)

            return response

        except stripe.StripeError as e:
            logging.error('error parsing data from stripe (stripe token = %s)' % (stripe_token))
            logging.error(smart_str(e))
            return HttpResponse(status=500)

    return HttpResponse(status=500) # I think it worked, but not sure why it's returning 500

@require_POST
@login_required
def cancel(request):
    try:
        request.user.customer.cancel()
        data = {}
    except stripe.StripeError as e:
        data = {"error": smart_str(e)}
    return _ajax_response(request, "payments/_cancel_form.html", **data)


@csrf_exempt
@require_POST
def webhook(request):
    data = json.loads(smart_str(request.body))
    if Event.objects.filter(stripe_id=data["id"]).exists():
        EventProcessingException.objects.create(
            data=data,
            message="Duplicate event record",
            traceback=""
        )
    else:
        event = Event.objects.create(
            stripe_id=data["id"],
            kind=data["type"],
            livemode=data["livemode"],
            webhook_message=data
        )
        event.validate()
        event.process()
    return HttpResponse()
