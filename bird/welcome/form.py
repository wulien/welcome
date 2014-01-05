from django import forms

class PhoneNoForm(forms.Form):
    phone_no = forms.CharField()
    verify_no = forms.CharField(required=False)