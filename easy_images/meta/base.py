from easy_images import utils


class MetaNotFound(Exception):
    pass


class Meta(object):
    """
    Base class for Easy Images Meta objects.
    """

    def __init__(self, settings):
        self.settings = utils.get_settings(settings)

    def get(self, options):
        raise NotImplementedError()
