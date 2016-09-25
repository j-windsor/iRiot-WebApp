from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Room
        fields = ('name',)
