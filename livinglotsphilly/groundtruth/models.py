from django.db import models
from django.utils.translation import ugettext_lazy as _

from livinglots_groundtruth.models import BaseGroundtruthRecord


class GroundtruthRecord(BaseGroundtruthRecord):

    use = models.ForeignKey('lots.Use',
        verbose_name=_('use'),
        limit_choices_to={'visible': False},
    )
