from . import conf_utils


class ImagesDict(conf_utils.SettingDict):
    """
    A group of settings that are used to process / retrieve images.

    These can be individually overridden in the project's settings module (with
    a dictionary, key names matching those settings you wish to override).
    """

    DEFAULT_OPTIONS = {'quality': 85}

    LEDGER = 'easy_images.ledger.DBLedger'
    QUEUE = 'easy_images.queue.RealtimeQueue'
    PROCESSOR = 'easy_images.processor.Processor'

    FILENAME = '{dir}{hash}{ext}'
    """
    The filename structure for processed images.

    The following string keyword arguments are available:

    dir
      The source directory
    hash
      A hash of the source and options
    name
      The base name of the source file (without a file extension)
    opts
      A string representation of the options used to generate this processed
      image
    ext
      The extension for the processed image
    """

    GENERATE_HIRES = False
    """
    Generate high-res versions of resized images if set to ``True``.
    """

    FALLBACK_URL = None
    """
    The fallback URL to use for images that aren't fully processed.
    """
    FALLBACK_SIZE = None
    """
    The dimensions of the fallback image.
    """


    STORAGE = ''
    """
    Which storage to use. If left blank, will use Django's default_storage.
    """

    SOURCES = [
        'easy_images.sources.pil.PILImage',
        # 'easy_images.sources.imagemagick.PDFImage',
    ]
    POST_PROCESSORS = [
        'easy_images.writer.post_processors.optimize',
    ]


class Settings(conf_utils.AppSettings):
    """
    These default settings can be specified in your Django project's settings
    module to alter the behaviour of easy-images.
    """

    IMAGES = ImagesDict
    """
    The main configuration dictionary for easy-images.
    """

    IMAGES_ALIASES = {}
    """
    A dictionary of aliased options.
    """

    IMAGES_MODULE_CACHE = 'default'
    """
    The Django cache to use for fast lookup of related module names.

    If set to ``None``, no cache will be used.
    """


settings = Settings()
