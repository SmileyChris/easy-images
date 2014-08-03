import hashlib

from django.db import models
from django.utils import timezone


class Storage(models.Model):
    python_path = models.CharField(max_length=255)

    def __str__(self):
        return self.python_path


class Source(models.Model):
    name = models.CharField(max_length=255)
    storage = models.CharField()
    date_modified = models.DateTimeField()

    def __str__(self):
        return self.name

    @property
    def source_hash(self):
        return hashlib.sha1('{storage_hash}:{source_hash}'.format(
            storage_hash=self.storage.storage_hash(),
            source_hash=hashlib.sha1(self.name).hexdigest(),
        ))


class QueueLock(models.Model):
    source = models.OneToOneField(Source)
    date_locked = models.DateTimeField(default=timezone.now)


class Ledger(models.Model):
    options_hash = models.CharField(max_length=100)
    source = models.ForeignKey(Source)
    name = models.CharField(max_length=255)
    date_processed = models.DateTimeField(null=True)
