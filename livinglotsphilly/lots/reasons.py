"""
Utilities dealing with the reasons a lot might be loaded into the database.
"""

from django.utils.safestring import mark_safe


def get_reasons(lot):
    reasons = []

    if lot.friendlyowner_set.exists():
        reasons.append({
            'short': 'added by user',
            'long': 'Someone told us that this lot is vacant and asked us to add it to the map.',
        })
    if lot.land_use_area and lot.land_use_area.category == 'Vacant or Other':
        reasons.append({
            'short': 'City Planning Commission land use vacant',
            'long': mark_safe('It is in the <a href="http://opendataphilly.org/opendata/resource/170/land-use/" target="_blank">City Planning Commission\'s Land Use database</a> marked as "%s".' % lot.land_use_area.description),
        })
    if lot.available_property and lot.available_property.status != 'no longer available':
        reasons.append({
            'short': 'PRA available property',
            'long': mark_safe('It is for sale as part of the Redevelopment Authority\'s <a href="http://secure.phila.gov/paplpublicweb/" target="_blank">Available Property list</a>.  <a href="https://secure.phila.gov/PAPLPublicWeb/AddAsset.aspx?AssetID=%s" target="_blank">Express interest</a> in this lot.' % lot.available_property.asset_id),
        })
    if lot.violations.count() > 0:
        reasons.append({
            'short': 'L&I violations',
            'long': mark_safe('It has <a href="http://www.phila.gov/data/Pages/default.aspx?entity=locationhistory&eid=%s" target="_blank">violations from Licensing and Inspections</a> that indicate that it is vacant.' % lot.violations.all()[0].location.external_id),
        })
    if lot.licenses.count() > 0:
        reasons.append({
            'short': 'L&I licenses',
            'long': mark_safe('It has <a href="http://www.phila.gov/data/Pages/LIPropertyHistory.aspx?entity=locationhistory&eid=%s" target="_blank">licenses from Licensing and Inspections</a> that indicate that it is vacant.' % lot.licenses.all()[0].location.external_id),
        })
    if lot.water_parcel and lot.water_parcel.percent_permeable > 50:
        reasons.append({
            'short': 'PWD mostly permeable',
            'long': mark_safe('The Water Department <a href="http://www.phila.gov/water/swmap/Parcel.aspx?parcel_id=%s" target="_blank">claims</a> that the parcel is %s%% permeable (without structures or pavement).' % (
                lot.water_parcel.parcel_id,
                lot.water_parcel.percent_permeable,
            ))
        })
    return reasons
