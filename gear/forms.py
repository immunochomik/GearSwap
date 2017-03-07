

from django import forms
from .models import Gear, GearImage


class GearAddForm(forms.ModelForm):

    class Meta:
        model = Gear
        fields = (
            'manufacturer',
            'manufacture_year',
            'model',
            'note',
            'tech_details',
            'qty',
            'rack_units',
            'form_factor',
            'state'
            )
        widgets = {
            'note':forms.Textarea
        }

class GearImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = GearImage
        fields = ('image', )
