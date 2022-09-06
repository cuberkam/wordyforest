from django.contrib.postgres.fields import ArrayField
from django.db import models


class Dictionary(models.Model):
    word = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)
    description = ArrayField(models.CharField(max_length=1000, blank=True))
    similars = ArrayField(models.CharField(max_length=1000, blank=True))
    antonyms = ArrayField(models.CharField(max_length=1000, blank=True))

    class Meta:
        ordering = ["word"]
        verbose_name_plural = "dictionaries"

    def __str__(self) -> str:
        return self.word
