import uuid

from django.db import models


class WordsList(models.Model):
    name = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)
    _words = models.CharField(max_length=10000, default=str)
    user = models.ForeignKey("users.CustomUser", models.CASCADE)
    is_private = models.BooleanField(default=True)
    share_id = models.CharField(
        max_length=50, unique=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        ordering = ["created_date"]
        verbose_name = "words_list"
        verbose_name_plural = "words_lists"
        unique_together = ["name", "user"]

    def __str__(self):
        return self.name

    @property
    def words(self):
        str_list = self._words.split(",")
        if str_list[0] != "":
            deneme = [int(i) for i in str_list]
            return deneme
        return []

    @words.setter
    def words(self, values):
        self._words = ",".join([str(x) for x in values])
        self.save()


class SubscribedList(models.Model):
    user = models.ForeignKey("users.CustomUser", models.CASCADE)
    words_list = models.ForeignKey(WordsList, models.CASCADE)

    class Meta:
        verbose_name = "subscribed_list"
        verbose_name_plural = "subscribed_lists"
        unique_together = ["user", "words_list"]

    def __str__(self):
        return f"{self.user} - {self.words_list}"
