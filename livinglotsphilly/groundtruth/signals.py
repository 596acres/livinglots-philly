from django.db.models.signals import post_save
from django.dispatch import receiver

import django_monitor
from django_monitor.util import save_handler

from .models import GroundtruthRecord


# Disconnect monitor's post-save handler. The view (subclass of
# monitor.views.MonitorMixin) will handle moderation
post_save.disconnect(save_handler, sender=GroundtruthRecord)

# Add our post-moderation handler
@receiver(django_monitor.post_moderation, sender=GroundtruthRecord,
          dispatch_uid='groundtruth_groundtruthrecord')
def update_use(sender, instance, **kwargs):
    """
    Once a GroundtruthRecord is moderated and approved, make it official by 
    updating the use on the referred-to Lot.
    """
    if not instance.is_approved or not instance.content_object:
        return

    lot = instance.content_object
    lot.known_use = instance.use
    lot.known_use_certainty = 10
    lot.known_use_locked = True
    lot.save()
