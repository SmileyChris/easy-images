import copy
import functools

from easy_images import utils
from easy_images.sources import filter_utils


def action(func):

    @functools.wraps(func)
    def dec(self, *args, **kwargs):
        new_source = copy.copy(self)
        new_source.img = func(self, *args, **kwargs)
        return new_source


class BaseSource(object):

    def __init__(self, source, image_settings):
        self.image_settings = image_settings
        processor_class = utils.get_obj(image_settings['PROCESSOR'])
        self.img = source
        self.processor = processor_class(source)

    @classmethod
    def from_file(cls, file_obj, image_settings):
        img = cls.read(file_obj)
        if img:
            return cls(img, image_settings)

    @staticmethod
    def read(file_obj):
        """
        Subclasses should override this method, taking a file-like object and
        returning an instance of the source image.
        """
        raise NotImplementedError()

    def process(self):
        self.processor(self.image_settings)

    @action
    def mode_grayscale(self, transparent, **kwargs):
        raise NotImplementedError()

    @action
    def mode_rgb(self, transparent, **kwargs):
        raise NotImplementedError()

    @action
    def replace_alpha(self, color, **kwargs):
        raise NotImplementedError()

    @action
    def whitespace_trim(self, **kwargs):
        raise NotImplementedError()

    @action
    def resize(self, size, **kwargs):
        raise NotImplementedError()

    @action
    def sharpen(self, strength, **kwargs):
        raise NotImplementedError()

    def size(self):
        raise NotImplementedError()

    def is_transparent(self):
        return False

    def is_grayscale(self):
        return False

    def is_rgb(self):
        return True

    def entropy(self):
        return 0
