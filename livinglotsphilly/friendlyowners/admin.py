from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from django_monitor.admin import MonitorAdmin

from livinglots_friendlyowners.admin import FriendlyOwnerAdminMixin

from .models import FriendlyOwner


class FriendlyOwnerAdmin(FriendlyOwnerAdminMixin, MonitorAdmin):
    fields = ('name', 'email', 'phone', 'notes', 'parcels', 'linked_lot',
              'added',)
    list_display = ('name', 'email', 'phone', 'linked_lot', 'added',)
    readonly_fields = FriendlyOwnerAdminMixin.readonly_fields + ('linked_lot',)

    def linked_lot(self, obj):
        if not obj.lot:
            return None
        return mark_safe(
            '<a href="%s">%s</a>' % (
                reverse('admin:lots_lot_change', args=(obj.lot.pk,)),
                str(obj.lot)
            )
        )
    linked_lot.short_description = 'Lot'


admin.site.register(FriendlyOwner, FriendlyOwnerAdmin)
