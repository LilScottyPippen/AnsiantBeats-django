from django.db import models
from django.core.validators import FileExtensionValidator


class Types(models.Model):
    title = models.CharField(max_length=30, db_index=True, default="title")

    def __str__(self):
        return self.title


class Tonal(models.Model):
    title = models.CharField(max_length=30, db_index=True, default="title")

    def __str__(self):
        return self.title
    

class Beat(models.Model):
    beat_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False)
    cover = models.FileField(blank=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    beat = models.FileField(blank=False, validators=[FileExtensionValidator(['mp3'])])
    type = models.ForeignKey(Types, on_delete=models.CASCADE)
    tonal = models.ForeignKey(Tonal, on_delete=models.CASCADE)
    duration = models.TimeField(null=True, blank=True)
    bpm = models.IntegerField(blank=False)
    price = models.FloatField(blank=False)

    def __str__(self):
        return self.title

