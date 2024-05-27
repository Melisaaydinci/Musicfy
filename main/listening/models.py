from django.db import models
from user.models import CustomUser
from music.models import Music
# Create your models here.
class MusicListening(models.Model):
    listener=models.ForeignKey(CustomUser,related_name='listener',on_delete=models.CASCADE)
    music=models.ForeignKey(Music,on_delete=models.CASCADE,related_name='music')
    listen_count=models.IntegerField(null=True,blank=True,default=0)