class Ledger(object):
    """
    """

    def get(self, source, image_settings):
        """
        Given a source (or source list).

        A source image can be a Django ``FieldFile`` class or a name.
        """
        options = utils.get_options(image_settings)
        fallback = self.get_fallback(image_settings)
        if not isiterable(source):
            return self._get(source_name, storage_name, options, fallback)
        for source_item in source:
            source.list

    def _get(self, source_name, storage_name, fallback=None):

    def options_string():
