from django.db import models
import librosa
import requests
import io


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
    cover = models.URLField(blank=False)
    beat = models.URLField(blank=False)
    type = models.ForeignKey(Types, on_delete=models.CASCADE)
    tonal = models.ForeignKey(Tonal, on_delete=models.CASCADE)
    duration = models.TimeField(null=True, blank=True)
    bpm = models.IntegerField(null=True, blank=True)
    price = models.FloatField(blank=False)

    def __str__(self):
        return self.title

    def get_bpm(self):
        audio_url = self.beat
        response = requests.get(audio_url)
        y, sr = librosa.load(io.BytesIO(response.content))
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr, hop_length=512, trim=False)
        self.bpm = tempo
        self.save()