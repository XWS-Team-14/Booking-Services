import uuid

from django.db import models

from .feature import Feature
from .location import Location


class Accommodation(models.Model):
    """Class used to model accommodation

    Attributes:
        id (UUID): Auto generated uuid used to uniquely indentify objects
        country (str): Name of the country where accommodation is located
        city (str): Name of the city where accommodation is located
        address (str): Address where the accommodation is located
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    features = models.ManyToManyField(Feature)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=False, blank=False)
    image_url = models.CharField(max_length=100, null=False, blank=False)
    min_guests = models.IntegerField(null=False, blank=False)
    max_guests = models.IntegerField(null=False, blank=False)
