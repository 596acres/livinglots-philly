from django.apps import AppConfig

from actstream import registry


class PhillyorganizeAppConfig(AppConfig):
    name = 'phillyorganize'

    def ready(self):
        super(PhillyorganizeAppConfig, self).ready()
        registry.register(self.get_model('Organizer'))
