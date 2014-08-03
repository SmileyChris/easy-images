class Aliases(object):
    """
    A container which stores and retrieves named easy-images settings
    dictionaries.
    """

    def __init__(self):
        """
        Initialize the Aliases object.
        """
        self._aliases = {}
        self.settings_loaded = False

    def load_settings(self):
        """
        Populate the aliases from the ``IMAGES_ALIASES`` setting.
        """
        from easy_images.conf import settings
        for name, alias_settings in settings.IMAGES_ALIASES.items():
            if name in self._aliases:
                continue
            self._aliases[name] = alias_settings
        self.settings_loaded = True

    def set(self, name, options):
        """
        Add an alias.

        :param name: The name of the alias to add.
        :param options: The options dictonary for this alias.
        """
        self._aliases[name] = options

    def get(self, name, load_settings=True):
        """
        Get a dictionary of aliased options.

        :param name: The name of the aliased options.

        If no matching alias is found, returns ``None``.
        """
        if not self.settings_loaded and load_settings:
            self.load_settings()
        return self._aliases.get(name)

    def all(self, load_settings=True):
        """
        Get a dictionary of all aliases and their options.
        """
        if not self.settings_loaded and load_settings:
            self.load_settings()
        return self._aliases


aliases = Aliases()
