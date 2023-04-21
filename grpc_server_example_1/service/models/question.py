import uuid
from django.db import models


class Question(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4(), editable=False)
    credit = models.CharField(max_length=100, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    contest_name = models.CharField(max_length=100, null=False, blank=False)
