from django.conf.urls import patterns, url

from .views import MailParticipantsView, MailParticipantsCountView

urlpatterns = patterns('',
    url(r'^participants/mail/$', MailParticipantsView.as_view(),
        name='mail_participants'),
    url(r'^participants/count/$', MailParticipantsCountView.as_view(),
        name='mail_participants_count'),
)
