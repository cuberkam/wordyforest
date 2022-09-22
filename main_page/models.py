from django.db import models


class Dictionary(models.Model):
    word = models.CharField(max_length=1000)
    type = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000, blank=True)
    example = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        ordering = ["word"]
        verbose_name = "dictionary"
        verbose_name_plural = "dictionaries"

    def __str__(self) -> str:
        return self.word


class Languages(models.Model):
    code = models.CharField(unique=True, max_length=10)
    eng_name = models.CharField(max_length=100)
    native_name = models.CharField(max_length=100)

    class Meta:
        ordering = ["code"]
        verbose_name = "language"
        verbose_name_plural = "languages"

    def __str__(self) -> str:
        return f"{self.code} : {self.eng_name}"
