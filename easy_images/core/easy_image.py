from easy_images import utils
from easy_images.alias import aliases


def get_ledger(alias_settings):
    cls = utils.get_obj(alias_settings['LEDGER'])
    return cls()


def get_queue(alias_settings):
    cls = utils.get_obj(alias_settings['QUEUE'])
    return cls()


class SettingsMixin(object):

    def __init__(self, image_settings=None, *args, **kwargs):
        self.image_settings = utils.get_settings(image_settings)
        super(SettingsMixin, self).__init__(
            image_settings=image_settings, *args, **kwargs)

    def get_settings(self, alias_or_settings):
        return utils.get_settings(self.image_settings, alias_or_settings)


class EasyImage(SettingsMixin):
    """
    The main image wrapper for the Easy Images package.
    """

    def __init__(self, source, storage=None, *args, **kwargs):
        self.source = source
        if storage is not None:
            self.base_settings['STORAGE'] = storage

    def __contains__(self, alias):
        """
        Check the legder to see if the alias has been generated already.
        """
        return bool(self.get_image(alias))

    def __getitem__(self, alias):
        """
        Get item from the ledger, or generate it.
        """
        return self.generate(alias)

    def get_image(self, alias_or_settings):
        alias_settings = self.get_settings(alias_or_settings)
        ledger = get_ledger(alias_settings)
        return ledger.get(self.source, alias_or_settings)   # TODO: or options?

    def generate(self, alias_or_settings):
        alias_settings = self.get_settings(alias_or_settings)
        queue = get_queue(alias_settings)
        return queue.generate(self.source, alias_settings)

    def generate_list(self, *alias_or_settings_list):
        """
        1. Split up source list into different queues.
        2. Generate each queue's source list, then reverse them.
        3. Iterate settings list again, popping off items from the matching
           queue list.
        """
        settings_list = []
        for alias_or_settings in alias_or_settings_list:
            settings_list.append(self.get_settings(alias_or_settings))

        queue_settings = {}
        for alias_settings in settings_list:
            queue_name = alias_settings['QUEUE']
            queue_settings_list = queue_settings.setdefault(queue_name, [])
            queue_settings_list.append(alias_settings)

        queue_processed = {}
        for queue_name, settings_list in queue_settings.items():
            queue = utils.get_obj(queue_name)()
            queue_processed[queue_name] = reversed(
                queue.generate(self.source, settings_list))

        processed_list = []
        for alias_settings in settings_list:
            img = queue_processed[alias_settings['QUEUE']].pop()
            processed_list.append(img)
        return processed_list

    def generate_all_aliases(self):
        return self.generate_list(*list(aliases))



class EasyImageList(object):
    """
    """
