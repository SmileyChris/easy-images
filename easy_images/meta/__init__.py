from easy_images import utils


class MetaNotFound(Exception):
    pass


class MetaOptions(object):

    def __init__(self, meta, options):
        self.meta = meta

    def options_hash(self):
        if not getattr(self, '_options_hash', None):
            self._options_hash =  = utils.get_options_hash(options)
        return self._options_hash

    def __bool__(self):
        return self.meta

    __nonzero__ = __bool__   # Python 2

    @property
    def url(self, image):
        if not image or self.meta.is_queued():
            return self.meta.settings.get('FALLBACK_URL', '')
        return image.queue.storage.get_url(image.name())

    def save(self, commit=False):
        return self.meta.save(self, commit=commit)




class Meta(object):

    def __init__(self, settings):
        self.settings = utils.get_settings(settings)
        self._bulk_save = {}

    def get(self, options):
        raise NotImplementedError()

    def write(self, options):
        raise NotImplementedError()

    def is_queued(self, meta_options):
        if meta_options.queued_time:
            timeout = options.get('QUEUE_OPTS', {}).get('timeout')
            if (
                    not timeout
                    or (meta_options.queued_time >=
                        timezone.now() - timedelta.timedelta(timeout)):
                return True
       return False

    def save(self, meta_options, commit=True):

    def bulk_save(self, meta_options_list):
        for meta_options in meta_options_list:
            self.save(meta_options)
