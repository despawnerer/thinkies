from django.forms import ModelForm, RadioSelect
from django.forms.models import ModelChoiceField

from users.models import User


class SettingsForm(ModelForm):
    default_identity = ModelChoiceField(
        queryset=None, widget=RadioSelect, empty_label=None)

    class Meta:
        model = User
        fields = ('default_identity',)

    def __init__(self, identities, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['default_identity'].queryset = identities
