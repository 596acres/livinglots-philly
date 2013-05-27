from django import forms

from notify.forms import NotifyOnCreationForm
from .models import StewardNotification


class StewardNotificationForm(NotifyOnCreationForm):

    class Meta:
        model = StewardNotification
        fields = (
            'name', 'phone', 'email', 'type', 'url', 'facebook_page',
            'use', 'land_tenure_status', 'support_organization',
            'others_get_involved', 'farm_stand', 'waiting_list', 'part_of_nga',
        )
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
