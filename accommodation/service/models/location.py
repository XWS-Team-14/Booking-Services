import uuid

from django.db import models


class Location(models.Model):
    """Class used to model location of a accommodation

    Attributes:
        id (UUID): Auto generated uuid used to uniquely indentify objects
        country (str): Name of the country where accommodation is located
        city (str): Name of the city where accommodation is located
        address (str): Address where the accommodation is located
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4(), editable=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
