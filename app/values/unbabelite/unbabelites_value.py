from app.values.unbabelite import UnbabeliteValue
from app.values.value_composite import ValueComposite

class UnbabelitesValues(ValueComposite):

    def __init__(self, unbabelites):
        super(UnbabeliteValue, self).initialize([])

        unbabelites_value = []
        for unbabelite in unbabelites:
                unbabelites_value.append(UnbabeliteValue(unbabelite.raw))

        self.serialize_and_append_from_values(unbabelites_value
