from app.values.unbabelite import UnbabeliteGeoJsonValue
from app.values.value_composite import ValueComposite


class UnbabelitesGeoJsonValue(ValueComposite):

    def __init__(self, unbabelites):
        super(UnbabelitesGeoJsonValue, self).initialize({})

        unbabelites_value = []
        for unbabelite in unbabelites:
                unbabelites_value.append(UnbabeliteGeoJsonValue(unbabelite).raw)

        self.serialize_with(type="FeatureCollection")
        self.serialize_with(crs={"type": "name", "properties": { "name": "unbabelites" }})
        self.serialize_with(features=unbabelites_value)

