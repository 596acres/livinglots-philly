from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from feincms.content.application import models as app_models
from feincms.models import Base

from livinglots_pathways.cms import PathwayFeinCMSMixin
from livinglots_pathways.models import BasePathway, BasePathwayManager


class PathwayManager(BasePathwayManager):

    def get_for_lot(self, lot):
        pathways = super(PathwayManager, self).get_for_lot(lot)

        # L&I filters
        licenses_exist = lot.licenses.count() != 0
        pathways = pathways.filter(Q(has_licenses=licenses_exist) |
                                   Q(has_licenses=None))

        # Violations
        violations_exist = lot.violations.count() != 0
        pathways = pathways.filter(Q(has_violations=violations_exist) |
                                   Q(has_violations=None))

        # If lot has violations, make sure the types match.
        pathways = pathways.filter(
            Q(violation_types__isnull=True) |
            Q(violation_types__in=lot.violations.values_list('violation_type__pk', flat=True))
        )

        # Available property filters
        is_available_property = lot.available_property is not None
        pathways = pathways.filter(Q(is_available_property=is_available_property) |
                                   Q(is_available_property=None))
        return pathways


class Pathway(PathwayFeinCMSMixin, BasePathway, Base):
    objects = PathwayManager()

    # Filters for determining which lots a pathway can apply to
    is_available_property = models.NullBooleanField(_('is available property'),
        help_text=_("Is the lot in the PRA's available property list?"),
    )
    has_licenses = models.NullBooleanField(_('has licenses from L&I'),
        help_text=_('Does the lot have vacancy-related licenses from L&I?'),
    )
    has_violations = models.NullBooleanField(_('has violations from L&I'),
        help_text=_('Does the lot have vacancy-related violations from L&I?'),
    )
    violation_types = models.ManyToManyField('violations.ViolationType',
        blank=True,
        null=True,
        help_text=_('This pathway applies to lots with these violation types.'),
    )

    @app_models.permalink
    def get_absolute_url(self):
        return ('pathway_detail', 'pathways.urls', (), {
            'slug': self.slug,
        })
