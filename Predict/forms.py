
from django.forms import ModelForm
from .models import Input
from django import forms
class InputForm(ModelForm):
    class Meta:
        model = Input
        fields = ['fullname', 'email', 'photo']

