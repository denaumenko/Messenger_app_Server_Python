from django.db import models

# Create your models here.

from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


class Notes(models.Model):
    title = models.CharField(max_length=50,null=False,blank=True)
    body = models.TextField(max_length=5000,null=True,blank=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    share_view = models.TextField(null=True,blank=True)
    share_edit = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title




