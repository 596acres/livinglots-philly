import json

from django import template

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag

from ..reasons import get_reasons

register = template.Library()


def express_interest_link(lot):
    point = lot.centroid.transform(3652, clone=True)
    return 'http://secure.phila.gov/PAPLPublicWeb/Mapview.aspx?_X=%f&_Y=%f' % (
        point.x,
        point.y
    )


def main_map_url(lot):
    default_filters = ('parents_only=True&known_use_existence=not+in+use&'
                       'known_use_existence=in+use&'
                       'available_property__status__in=new+and+available&'
                       'available_property__status__in=available&'
                       'view_type=tiles&owner__owner_type__in=mixed&'
                       'owner__owner_type__in=private&'
                       'owner__owner_type__in=public')
    centroid = json.dumps({
        'lat': lot.centroid.y,
        'lng': lot.centroid.x,
    })
    return '/?%s&centroid=%s&zoom=18' % (default_filters, centroid)


class GetVacantReasons(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, lot):
        return get_reasons(lot)


register.filter('express_interest_link', express_interest_link)
register.filter('main_map_url', main_map_url)
register.tag(GetVacantReasons)
