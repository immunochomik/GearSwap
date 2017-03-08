

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
            'state',
            'main_image'
            )
        widgets = {
            'note':forms.Textarea(),
            'qty':forms.NumberInput({'value':'1'}),
            'rack_units':forms.NumberInput({'value':'0'}),
        }


class GearImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = GearImage
        fields = ('image', )
