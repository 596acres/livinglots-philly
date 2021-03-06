from django.apps import AppConfig

from actstream import registry


class LotsAppConfig(AppConfig):
    name = 'lots'

    def ready(self):
        super(LotsAppConfig, self).ready()
        registry.register(self.get_model('Lot'))
        registry.register(self.get_model('LotGroup'))
        import signals
