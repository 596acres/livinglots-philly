from django import forms
from django.utils.translation import ugettext_lazy as _

from livinglots_usercontent.notes.models import Note
from libapps.organize import forms as organize_forms


class OrganizerForm(organize_forms.OrganizerForm):
    note = forms.CharField(
        help_text=_('Enter a public note to let your neighbors know what you '
                    'would like to do on this lot'),
        required=False,
        widget=forms.Textarea(),
    )

    def clean(self):
        cleaned_data = super(OrganizerForm, self).clean()
        email = cleaned_data.get('email', None)
        phone = cleaned_data.get('phone', None)
        if not (email or phone):
            raise forms.ValidationError(_('Please enter an email address or '
                                          'phone number'))
        return cleaned_data

    def save_note(self, organizer, note=None, name=None, **kwargs):
        if not (note and name):
            return None
        saved_note = Note(
            added_by_name=name,
            content_object=organizer.content_object,
            text=note,
        )
        saved_note.save()
        return saved_note

    def save(self, *args, **kwargs):
        organizer = super(OrganizerForm, self).save(*args, **kwargs)
        self.save_note(organizer, **self.cleaned_data)
        return organizer

    class Meta(organize_forms.OrganizerForm.Meta):
        exclude = ('notes',)
