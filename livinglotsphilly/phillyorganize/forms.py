from django import forms
from django.utils.translation import ugettext_lazy as _

from libapps.organize import forms as organize_forms


class OrganizerForm(organize_forms.OrganizerForm):

    def clean(self):
        cleaned_data = super(OrganizerForm, self).clean()
        email = cleaned_data.get('email', None)
        phone = cleaned_data.get('phone', None)
        if not (email or phone):
            raise forms.ValidationError(_('Please enter an email address or '
                                          'phone number'))
        return cleaned_data

    class Meta(organize_forms.OrganizerForm.Meta):
        exclude = ('notes',)
