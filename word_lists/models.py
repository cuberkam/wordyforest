from django.db import models


class WordLists(models.Model):
    list_name = models.CharField(max_length=50, unique=True)
    created_date = models.DateField(auto_now_add=True)
    word = models.ManyToManyField("main_page.Dictionary")

    class Meta:
        ordering = ["list_name"]
        verbose_name_plural = "word_lists"

    def __str__(self):
        return self.list_name
