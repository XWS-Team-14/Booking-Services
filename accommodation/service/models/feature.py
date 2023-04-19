import uuid

from django.db import models


class Feature(models.Model):
    """Class used to model feautres of a accommodation

    Attributes:
        id (UUID): Auto generated uuid used to uniquely indentify objects
        feature (str): Name of the feautre
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4(), editable=False)
    feature = models.CharField(max_length=100, null=False, blank=False)
