from easy_images import utils


class ProcessedImage(object):

    def __init__(self, ledger, content=None):
        self.ledger = ledger
        self.content = content

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        self._has_content = value is not None

    @property
    def has_content(self):
        return getattr(self, '_has_content')

    @property
    def options(self):
        if not hasattr(self, '_options'):
            self._options = utils.get_options(self.ledger.alias)
        return self._options

    def save(self):
        if not self.has_content:
            raise ValueError("ProcessedImage does not contain content")
        name = self.options.storage.save(self.content)
        if name != self.ledger.name:
            self.ledger.name = name
            if self.ledger.pk:
                self.ledger.save()

    save.alters_data = True

