from easy_images import utils
from easy_images.meta import base
from easy_images.meta.database.easy_images_meta_db import models


class DatabaseMeta(base.Meta):

    def get(self, options):
        utils.options_hash(options)
        try:
            return models.Meta.objects.get(hash=options_hash)
        except models.Meta.DoesNotExist:
            raise base.MetaNotFound()
