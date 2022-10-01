from django.contrib.postgres.fields import ArrayField
from django.db import models


class WordsList(models.Model):
    name = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)
    words = ArrayField(models.IntegerField(), null=True, default=list)
    user = models.ForeignKey("users.CustomUser", models.CASCADE)
    is_private = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "words_list"
        verbose_name_plural = "words_lists"
        unique_together = ["name", "user"]

    def __str__(self):
        return self.name
