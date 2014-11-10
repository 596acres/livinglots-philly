from admin_tools.dashboard import modules

from django.db.models import Count

from phillydata.owners.models import Owner


class LotsByOwnerModule(modules.DashboardModule):
    count = 15
    owner_type = 'public'
    template = 'lots/admin_dashboard/by_owner.html'
    title = 'Lots by Owner'

    def init_with_context(self, context):
        owners = Owner.objects.filter(lot__isnull=False, owner_type=self.owner_type) \
                .annotate(lots=Count('lot')) \
                .order_by('-lots', 'name')
        context['owners'] = owners[:self.count]
        return context
