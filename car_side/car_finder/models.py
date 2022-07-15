from pathlib import Path

from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string

def image_path(instance, filename) -> str:
    name = instance.name.__str__() + '.jpg'
    return Path(settings.MEDIA_ROOT).joinpath(name).as_posix()

def output_image_path(instance, filename) -> str:
    name = instance.name.__str__() + '.jpg'
    return Path(settings.MEDIA_ROOT).joinpath(name).as_posix()

class CarImage(models.Model):
    name =  models.CharField(max_length=100,
                              default=get_random_string(length=32))
    image = models.ImageField(upload_to= image_path)
    output_image = models.ImageField(upload_to= output_image_path, default=None)
    number_of_cars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    