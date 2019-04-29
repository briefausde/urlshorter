from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Url(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    original_url = models.CharField(max_length=1024)
    short_url = models.CharField(max_length=12)

    @property
    def clicks(self):
        return len(Click.objects.filter(url=self))

    def __str__(self):
        return 'Link shortened to {}'.format(self.short_url)


class Click(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Click on {}'.format(self.date.strftime("%b %d %Y %H:%M:%S"))
