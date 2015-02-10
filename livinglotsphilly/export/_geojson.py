import geojson


title = 'geojson'
extensions = ('geojson',)


def export_set(dataset):
    """Returns GeoJSON representation of Dataset."""
    features = []
    for row in dataset.dict:
        features.append(geojson.Feature(
            geometry=geojson.Point(coordinates=[
                float(row['longitude']),
                float(row['latitude'])
            ]),
            properties=row,
        ))
    return geojson.dumps(geojson.FeatureCollection(features))


#
# Add our geojson format to tablib
#

from tablib.core import Dataset

setattr(Dataset, title, property(export_set))
