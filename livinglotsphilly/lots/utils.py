from phillydata.waterdept.models import WaterParcel

from .models import Lot


def _fix_water_parcel(lot):
    try:
        # Find and set to new one
        lot.water_parcel = WaterParcel.objects.get(parcelid=lot.water_parcel.parcel_id)
    except WaterParcel.DoesNotExist:
        return

    # Update geometry
    lot.polygon = lot.water_parcel.geometry
    lot.centroid = lot.polygon.centroid
    lot.save()


def fix_water_parcels(count=1000):
    """
    Fix lots' water parcels.

    Point to new water parcels where available since these have geometries and
    are generally more updated.
    """
    lots_with_old_water_parcels = Lot.objects.filter(
        water_parcel__isnull=False,
        water_parcel__parcelid__isnull=True,
    )
    for lot in lots_with_old_water_parcels[:count]:
        _fix_water_parcel(lot)
