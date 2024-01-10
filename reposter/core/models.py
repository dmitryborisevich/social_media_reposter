import os
from django.db import models


class Source(models.Model):
    url = models.URLField(unique=True)
    post_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    instagram_published = models.BooleanField(default=False)
    vk_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.name}"


def get_path(instance, filename):
    return os.path.join(f'media/images/{instance.source.id}/', f'{instance.id}.jpg')


class Image(models.Model):
    image = models.ImageField(upload_to=get_path)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
