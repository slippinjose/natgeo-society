from app.values.value_composite import ValueComposite


class UnbabeliteValue(ValueComposite):

    def __init__(self, unbabelite):
        super(UnbabeliteValue, self).initialize({})

        self.serialize_with(employee_id=unbabelite.employee_id)
        self.serialize_with(name=unbabelite.name)
        self.serialize_with(country=unbabelite.country)
        self.serialize_with(city=unbabelite.city)
        self.serialize_with(coordinates=unbabelite.coordinates)
        self.serialize_with(photo=unbabelite.photo)

        self.serialize_with(role=self._role(unbabelite))
        self.serialize_with(position=unbabelite.position)

    def _role(self, unbabelite):
        if not unbabelite.position and not unbabelite.team:
            return ''

        if unbabelite.position and not unbabelite.team:
            return unbabelite.position

        if unbabelite.position and unbabelite.team:
            return f"{unbabelite.position}, {unbabelite.team}"
