from django.forms import ModelForm
from django import forms
from .models import *


class ChatmessagesCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add message ...', 'class': 'p-4 text-black', 'maxlegth' : '300', 'autofocus' : True})
        }