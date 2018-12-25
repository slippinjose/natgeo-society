from app.values.value_composite import ValueComposite


class UnbabeliteGeoJsonValue(ValueComposite):

    def __init__(self, unbabelite):
        super(UnbabeliteGeoJsonValue, self).initialize({})

        self.serialize_with(type='Feature')
        self.serialize_with(geometry={
            "type": "Point",
            "coordinates": [unbabelite.lng, unbabelite.lat]
        })
        self.serialize_with(properties={
            "name": unbabelite.name,
            "city": unbabelite.city,
            "country": unbabelite.country
        })
