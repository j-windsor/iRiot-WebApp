from django import forms
from .models import Hub

class HubForm(forms.ModelForm):
    alias = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Hub
        fields = ('alias','serial_number')
