from django.db import models
from django.contrib.auth.models import User


class Integration(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="integration"
    )
    access_token = models.CharField(max_length=256, blank=True)
    refresh_token = models.CharField(max_length=256, blank=True)
    integration_user_id = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f"Integration for {self.user}"


class AlbumPlaylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    class Meta:
        unique_together = ("user", "name")


class Album(models.Model):
    playlist = models.ManyToManyField(AlbumPlaylist)
    name = models.CharField(max_length=256)
    total_tracks = models.PositiveSmallIntegerField()
    spotify_id = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return f"{self.name} ({self.total_tracks} tracks)"
