from django import forms

from ajaximage.widgets import AjaxImageWidget


class AjaxImageUploadForm(forms.Form):
    image = forms.CharField(widget=AjaxImageWidget(upload_to='uploads'))