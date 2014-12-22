from django import forms

from livinglots_groundtruth.forms import GroundtruthRecordFormMixin

from .models import GroundtruthRecord


class GroundtruthRecordForm(GroundtruthRecordFormMixin, forms.ModelForm):

    class Meta:
        fields = (
            'content_type',
            'object_id',
            'actual_use',
            'contact_name',
            'contact_email',
            'contact_phone',
            'use',
        )

        model = GroundtruthRecord
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
            'use': forms.HiddenInput(),
        }
