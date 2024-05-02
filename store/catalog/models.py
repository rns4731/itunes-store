from django.db import models
from model_utils.models import TimeStampedModel


class Artist(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Album(TimeStampedModel):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=False, related_name='albums')
    name = models.CharField(max_length=255)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class Track(TimeStampedModel):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=False, related_name='tracks')
    title = models.CharField(max_length=255, null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.title}"