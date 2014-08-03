from django.db import models


class Meta(models.Model):
    name = models.CharField(max_length=250)
    queued = models.BooleanField()
    created = models.DateTimeField()
    source_hash = models.CharField(max_length=40, db_index=True)
    options_hash = models.CharField(max_length=40, db_index=True)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    # size = models.PositiveIntegerField()
