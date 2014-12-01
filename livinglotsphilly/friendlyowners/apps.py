from django.apps import AppConfig
from django.db.models.signals import post_save

import django_monitor
from django_monitor.util import save_handler


class FriendlyOwnersAppConfig(AppConfig):
    name = 'friendlyowners'

    def ready(self):
        super(FriendlyOwnersAppConfig, self).ready()

        FriendlyOwner = self.get_model('FriendlyOwner')
        django_monitor.nq(FriendlyOwner)

        # Disconnect monitor's post-save handler, moderation will be handled in
        # the view
        post_save.disconnect(save_handler, sender=FriendlyOwner)

        from .signals import *
