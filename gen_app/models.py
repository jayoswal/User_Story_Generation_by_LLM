from django.db import models
from django import forms

class InputForm(forms.Form):
    inp_prompt = forms.CharField(widget=forms.Textarea)
