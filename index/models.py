from django.db import models
import librosa
import requests
import io


class Types(models.Model):
    title = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Tonal(models.Model):
    title = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Beat(models.Model):
    beat_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False)
    cover = models.URLField(blank=False, default='https://drive.google.com/uc?id=')
    beat = models.URLField(blank=False, default='https://drive.google.com/uc?id=')
    type = models.ForeignKey(Types, on_delete=models.CASCADE)
    tonal = models.ForeignKey(Tonal, on_delete=models.CASCADE)
    duration = models.CharField(max_length=10, null=True, blank=True)
    bpm = models.IntegerField(null=True, blank=True)
    price = models.FloatField(blank=False)

    def __str__(self):
        return self.title

    def get_bpm_and_duration(self):
        if self.duration is None and self.bpm is None:
            audio_url = self.beat
            response = requests.get(audio_url)
            y, sr = librosa.load(io.BytesIO(response.content))
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr, hop_length=512, trim=False)
            duration = librosa.get_duration(y=y, sr=sr)
            minutes, seconds = divmod(duration, 60)
            self.bpm = tempo
            if len(str(minutes)) == 4:
                self.duration = f'{int(minutes):d}:{int(seconds):02d}'
            else:
                self.duration = f'0{int(minutes):d}:{int(seconds):02d}'
            self.save()


class License(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name
