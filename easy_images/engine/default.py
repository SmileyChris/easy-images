from easy_images.conf import settings
from django.utils.module_loading import import_string

# Set the default engine.
default_engine = import_string(settings.EASY_IMAGES__ENGINE)()  # noqa


def get_default_storage():
    storage_setting = settings.EASY_IMAGES__STORAGE
    if storage_setting:
        return import_string(storage_setting)()
    from django.core.files.storage import default_storage
    return default_storage


# Set the default storage.
default_storage = get_default_storage()
