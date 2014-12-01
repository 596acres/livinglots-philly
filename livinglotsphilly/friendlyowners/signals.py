from django.dispatch import receiver

from django_monitor import post_moderation

from livinglots_notify.helpers import notify_facilitators

from lots.models import Lot
from .models import FriendlyOwner


@receiver(post_moderation, sender=FriendlyOwner,
          dispatch_uid='friendlyowners_friendlyowner_notify')
def notify(sender, instance=None, **kwargs):
    """
    Notify facilitators if the instance is pending.
    """
    if instance and instance.is_pending:
        notify_facilitators(instance)


@receiver(post_moderation, sender=FriendlyOwner,
          dispatch_uid='friendlyowners_friendlyowner')
def add_lot(sender, instance, **kwargs):
    """
    Once a FriendlyOwner is moderated and approved, make it official by adding
    the lot.
    """
    if not instance.is_approved:
        return

    lot = Lot.objects.create_lot_for_parcels(instance.parcels.all())
    lot.known_use = None
    lot.known_use_certainty = 10
    lot.known_use_locked = True
    lot.owner_opt_in = True
    lot.friendlyowner_set.add(instance)
    lot.save()
