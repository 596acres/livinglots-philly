from django.contrib.contenttypes.models import ContentType
from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from livinglots_genericviews import JSONResponseView
from livinglots_organize.mail import mass_mail_organizers

from phillyorganize.models import Organizer

from lots.models import Lot
from lots.views import FilteredLotsMixin


class FilteredOrganizersMixin(FilteredLotsMixin):

    def get_organizers(self):
        lot_pks = self.get_lots(visible_only=True).values_list('pk', flat=True)
        return Organizer.objects.filter(
            content_type=ContentType.objects.get_for_model(Lot),
            object_id__in=lot_pks,
        ).distinct()


class MailParticipantsView(FilteredOrganizersMixin, LoginRequiredMixin,
                           PermissionRequiredMixin, JSONResponseView):
    permission_required = ('organize.email_participants')

    def get(self, request, *args, **kwargs):
        self.subject = request.GET.get('subject', None)
        self.message = request.GET.get('text', None)
        self._mail_organizers(self.subject, self.message)
        return super(MailParticipantsView, self).get(request, *args, **kwargs)

    def _mail_organizers(self, subject, message):
        self.organizers = self.get_organizers()
        self.organizers = self.organizers.exclude(email='')
        mass_mail_organizers(subject, message, self.organizers)

    def get_context_data(self, **kwargs):
        return {
            'emails': len(set(self.organizers.values_list('email', flat=True))),
            'organizers': self.organizers.count(),
            'subject': self.subject,
        }


class MailParticipantsCountView(FilteredOrganizersMixin, JSONResponseView):

    def get_context_data(self, **kwargs):
        organizers = self.get_organizers()
        return {
            'emails': len(set(organizers.values_list('email', flat=True))),
            'organizers': organizers.count(),
        }


class ExtraAdminIndex(LoginRequiredMixin, PermissionRequiredMixin,
                      TemplateView):
    # Either require ALL permissions required to perform actions on this page
    # or require ONE of them, filter template accordingly
    permission_required = ('organize.email_participants',)
    template_name = 'extraadmin/index.html'
