from django.core.exceptions import RequestDataTooBig
from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField("Telegram Id for user", unique=True)
    telegram_name = models.CharField("Telegram id of user",max_length=32, unique=True)
    

class SearchArea(models.Model):
    name = models.CharField(max_length=80, unique=True)


class SearchRequest(models.Model):
    request = models.TextField("Geo Request")
    result = models.TextField("Result of request")
    date = models.DateTimeField("Date of request", auto_now_add=True)
    user = models.ForeignKey(to=TelegramUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.request
