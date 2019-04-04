class UpdateUnbabeliteProfileService(object):

    def __init__(self, unbabelite, **kwargs):
        self.unbabelite = unbabelite
        self.kwargs = kwargs

    def call(self):
        self.unbabelite.update(**self.kwargs)
