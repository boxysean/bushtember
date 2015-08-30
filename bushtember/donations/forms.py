from django import forms


class ImageUploadForm(forms.Form):
    # image = forms.CharField(widget=AjaxImageWidget(upload_to='uploads'))
    image = forms.ImageField()