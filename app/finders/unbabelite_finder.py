from app.models import Unbabelite


class UnbabeliteFinder(object):

    @staticmethod
    def get_from_name(name):
        return Unbabelite.query.filter_by(name=name).all()
