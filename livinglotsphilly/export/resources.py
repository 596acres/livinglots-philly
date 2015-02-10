from import_export.fields import Field
from import_export.resources import ModelResource

from lots.models import Lot


class LotResource(ModelResource):
    address = Field(attribute='address_line1')
    area = Field(attribute='polygon_area')
    brt_account = Field(attribute='water_parcel__brt_account',
                        column_name='brt / opa account')
    city = Field(attribute='city')
    council_district = Field(attribute='city_council_district__label',
                             column_name='city council district')
    is_vacant = Field(column_name='is vacant?')
    latitude = Field()
    longitude = Field()
    owner = Field(attribute='owner__name')
    owner_type = Field(attribute='owner__owner_type', column_name='owner type')
    planning_district = Field(attribute='planning_district__label',
                              column_name='planning district')
    state = Field(attribute='state_province')
    ten_code = Field(attribute='water_parcel__ten_code', column_name='ten code')
    use = Field(attribute='known_use__name')
    zip_code = Field(attribute='postal_code', column_name='zip code')

    # TODO why is the lot here?
    # TODO zip code is not always populated?

    class Meta:
        model = Lot
        export_order = (
            'ten_code',
            'brt_account',
            'owner',
            'owner_type',
            'address',
            'city',
            'state',
            'zip_code',
            'area',
            'is_vacant',
            'use',
            'council_district',
            'planning_district',
            'longitude',
            'latitude',
        )
        fields = (
            'pk',
        )

    def get_queryset(self):
        qs = self._meta.model.objects.get_visible()
        qs = qs.select_related('city_council_district', 'owner',
                               'planning_district', 'water_parcel')
        qs = qs.filter(centroid__isnull=False)
        return qs

    def dehydrate_is_vacant(self, lot):
        try:
            if not lot.known_use:
                return 'yes'
        except Exception:
            pass
        return 'no'

    def dehydrate_latitude(self, lot):
        if lot.centroid:
            return round(lot.centroid.y, 6)
        return None

    def dehydrate_longitude(self, lot):
        if lot.centroid:
            return round(lot.centroid.x, 6)
        return None
