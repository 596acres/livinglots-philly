from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import StewardNotification


class StewardNotificationForm(forms.ModelForm):
    name = forms.CharField(
        max_length=256,
        label = _('Garden name'),
        help_text=_('The name of the project using this lot.')
    )

    class Meta:
        model = StewardNotification
        fields = (
            # Hidden fields
            'content_type', 'object_id',

            # Organizer fields
            'name', 'phone', 'email', 'type', 'url', 'facebook_page',

            # StewardProject fields
            'use', 'land_tenure_status', 'support_organization',
            'include_on_map', 'share_contact_details',
        )
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
