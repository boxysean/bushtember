from django import forms

from .settings import PLAN_CHOICES


class PlanForm(forms.Form):
    # pylint: disable=R0924
    plan = forms.ChoiceField(choices=PLAN_CHOICES + [("", "-------")])


class DonateForm(forms.Form):
    name = forms.CharField(label='Your name')
    amount = forms.DecimalField(widget=forms.HiddenInput()) # some validation done on javascript, this form is taking the results from stripe, which itself will complain...

    def clean(self):
        cleaned_data = super(DonateForm, self).clean()

        if cleaned_data['amount'] <= 0.5:
            raise forms.ValidationError('amount must be greater than 50 cents')
