import importlib

import six

from easy_images.alias import aliases


def get_settings(image_settings=None, alias_settings=None):
    """
    Get easy-image settings.

    :param image_settings: The base image settings dictionary to use (uses
        ``settings.IMAGES`` if not provided).
    :param alias_settings: An alias name or options dictionary to use to
        override the base image settings (optional).
    """
    if image_settings is None:
        from easy_images.conf import settings
        image_settings = settings.IMAGES
    image_settings = image_settings.copy()
    if alias_settings:
        if isinstance(alias_settings, six.text):
            # If text, look up the alias options.
            if alias_settings not in aliases:
                raise ValueError('No alias named "{0}"'.format(alias_settings))
            alias_settings = aliases[alias_settings]
        image_settings.extend(alias_settings)
    return image_settings


def get_options(alias_settings):
    options = {}
    for key, value in alias_settings.values():
        if key == key.lower():
            options[key] = value
    return options


def get_obj(name):
    module_name, obj_name = name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, obj_name)
