from django import forms
from django.utils.translation import ugettext_lazy as _

from livinglots_friendlyowners.forms import FriendlyOwnerFormMixin

from phillydata.waterdept.models import WaterParcel

from .models import FriendlyOwner


class FriendlyOwnerForm(FriendlyOwnerFormMixin, forms.ModelForm):

    parcels = forms.ModelMultipleChoiceField(
        WaterParcel.objects.all(),
        error_messages={
            'required': _('Please select a parcel.'),
        },
        widget=forms.MultipleHiddenInput()
    )

    class Meta:
        model = FriendlyOwner
        exclude = ('lot',)
