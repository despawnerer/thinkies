from django.forms import ModelForm
from django.forms.widgets import Textarea

from opinions.models import Tip


class TipForm(ModelForm):
    class Meta:
        model = Tip
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'placeholder': "Leave a tip for others"})
        }
