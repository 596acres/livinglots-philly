from import_export.fields import Field
from import_export.resources import ModelResource

from lots.models import Lot


class LotResource(ModelResource):
    address = Field(attribute='address_line1')
    area = Field(attribute='polygon_area')
    brt_account = Field(attribute='water_parcel__brt_account')
    city = Field(attribute='city')
    council_district = Field('city_council_district__label')
    is_vacant = Field()
    latitude = Field(attribute='centroid__y')
    longitude = Field(attribute='centroid__x')
    owner = Field(attribute='owner__name')
    owner_type = Field(attribute='owner__owner_type')
    planning_district = Field(attribute='planning_district__label')
    state = Field(attribute='state_province')
    ten_code = Field(attribute='water_parcel__ten_code')
    use = Field(attribute='known_use__name')
    zip_code = Field(attribute='postal_code')

    # TODO why is the lot here?
    # TODO zip code is not always populated?

    class Meta:
        model = Lot
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
