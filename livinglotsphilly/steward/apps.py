from django.apps import AppConfig

import django_monitor


class StewardAppConfig(AppConfig):
    name = 'steward'

    def ready(self):
        super(StewardAppConfig, self).ready()
        django_monitor.nq(self.get_model('StewardNotification'))
        import signals
