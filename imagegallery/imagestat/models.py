from django.db import models
from cloudinary.models import CloudinaryField


class User(models.Model):
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=256)
    date_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Images(models.Model):
    description = models.CharField(max_length=512, blank=True, null=True)
    path = CloudinaryField(max_length=512, blank=True)
    time = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'images'


class Sessions(models.Model):
    session_id = models.CharField(primary_key=True, max_length=128)
    expires = models.PositiveIntegerField()
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Images, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    date_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'
