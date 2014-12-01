from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard

from lots.admin_dashboard import LotsByOwnerModule
from phillyorganize.admin_dashboard import EditEmailsModule


class PhillyDashboard(Dashboard):
    columns = 3

    def __init__(self, **kwargs):

        self.children = self.children or []

        self.children.append(LotsByOwnerModule(
            owner_type='public',
            title=_('Top Public Owners'),
        ))

        self.children.append(LotsByOwnerModule(
            owner_type='private',
            title=_('Top Private Owners'),
        ))

        self.children.append(EditEmailsModule())

        self.children.append(modules.ModelList(
            title=_('Site Content'),
            models=(
                'elephantblog.*',
                'feincms.module.page.*',
                'pathways.*',
            ),
        ))

        self.children.append(modules.ModelList(
            title=_('Lots'),
            models=(
                'lots.*',
            ),
        ))

        self.children.append(modules.ModelList(
            title=_('Organize'),
            models=(
                'phillyorganize.*',
            ),
        ))

        self.children.append(modules.AppList(
            title=_('Applications'),
            exclude=(
                'django.contrib.*',
                'elephantblog.*',
                'feincms.module.page.*',
                'phillydata.*',
                'livinglots_usercontent.*',
                'lots.*',
            ),
        ))

        self.children.append(modules.ModelList(
            title=_('Lot Content'),
            models=('livinglots_usercontent.*',),
        ))

        self.children.append(modules.AppList(
            title=_('Data'),
            models=('phillydata.*',),
        ))

        self.children.append(modules.AppList(
            title=_('Administration'),
            models=('django.contrib.*',),
        ))

        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            limit=5
        ))
