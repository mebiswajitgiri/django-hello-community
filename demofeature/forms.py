from django import forms
from .models import DemoModel02

class DemoForm(forms.ModelForm):
    class Meta:
        model = DemoModel02
        fields = "__all__"