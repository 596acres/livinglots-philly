from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Lot


@receiver(pre_save, sender=Lot)
def save_lot_update_group(sender, instance=None, **kwargs):
    """Update the group that this member is part of."""
    if not instance: return

    # Try to get the group this instance was part of, if any
    try:
        previous_group = Lot.objects.get(pk=instance.pk).group
    except Exception:
        previous_group = None

    # Get the group this instance will be part of, if any
    next_group = instance.group

    # If instance was in a group before but no longer will be, update that
    # group accordingly
    if previous_group and previous_group != next_group:
        previous_group.remove(instance)

    # If instance was not in a group before but will be, update that group
    if next_group and next_group != previous_group:
        next_group.add(instance)


@receiver(post_delete, sender=Lot)
def delete_lot_update_group(sender, instance=None, **kwargs):
    if instance.group:
        instance.group.update()
