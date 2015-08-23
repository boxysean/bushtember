from django import forms

from .settings import PLAN_CHOICES


class PlanForm(forms.Form):
    # pylint: disable=R0924
    plan = forms.ChoiceField(choices=PLAN_CHOICES + [("", "-------")])


class DonateForm(forms.Form):
    amount = forms.DecimalField() # TODO: improve

    def clean(self):
        cleaned_data = super(DonateForm, self).clean()

        if cleaned_data['amount'] <= 0:
            raise forms.ValidationError('amount must be greater than zero')
