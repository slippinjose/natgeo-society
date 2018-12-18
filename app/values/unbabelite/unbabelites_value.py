from app.values.unbabelite import UnbabeliteValue
from app.values.value_composite import ValueComposite


class UnbabelitesValue(ValueComposite):

    def __init__(self, unbabelites):
        super(UnbabelitesValue, self).initialize([])

        unbabelites_value = []
        for unbabelite in unbabelites:
                unbabelites_value.append(UnbabeliteValue(unbabelite))

        self.serialize_and_append_from_values(unbabelites_value)
