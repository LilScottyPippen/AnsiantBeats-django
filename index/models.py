import datetime

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


class Mood(models.Model):
    title = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return self.title


class Beat(models.Model):
    beat_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False)
    cover = models.URLField(blank=False)
    beat = models.URLField(blank=False)
    type = models.ForeignKey(Types, on_delete=models.CASCADE)
    tonal = models.ForeignKey(Tonal, on_delete=models.CASCADE)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, null=True)
    isGold = models.BooleanField(default=False)
    isNew = models.BooleanField(default=True)
    isPlaylist = models.BooleanField(default=True)
    duration = models.CharField(max_length=10, null=True, blank=True)
    bpm = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(blank=False)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=False)

    def __str__(self):
        return self.title

    def get_bpm_and_duration(self):
        try:
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
        except Exception as e:
            print(e)

    def convert_drive_link(self):
        try:
            if self.cover.startswith('https://drive.google.com/file/d/'):
                file_id = self.cover.split('/d/')[1].split('/')[0]
                preview_link = f'https://drive.google.com/uc?id={file_id}'
                self.cover = preview_link
                self.save()
            if self.beat.startswith('https://drive.google.com/file/d/'):
                file_id = self.beat.split('/d/')[1].split('/')[0]
                preview_link = f'https://drive.google.com/uc?id={file_id}'
                self.beat = preview_link
                self.save()
        except Exception as e:
            print(e)

    def basic_price(self):
        first_level_license = License.objects.get(license_level=1)
        return self.price + first_level_license.price


class License(models.Model):
    name = models.CharField(max_length=100)
    license_level = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} | {self.subject} | {self.email}'


class Coupon(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    discount = models.IntegerField()

    def __str__(self):
        return self.title
