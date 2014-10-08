from django.apps import AppConfig

from actstream import registry
import django_monitor


class GroundtruthAppConfig(AppConfig):
    name = 'groundtruth'

    def ready(self):
        super(GroundtruthAppConfig, self).ready()
        GroundtruthRecord = self.get_model('GroundtruthRecord')
        registry.register(GroundtruthRecord)
        django_monitor.nq(GroundtruthRecord)

        import signals
