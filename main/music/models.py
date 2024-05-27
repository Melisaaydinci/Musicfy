from django.db import models
from datetime import datetime

class Music(models.Model):
    id=models.CharField(max_length=200, unique=True,primary_key=True)
    title=models.CharField(max_length=200)
    release=models.CharField(max_length=200)
    artist_name=models.CharField(max_length=200)
    year=models.IntegerField(null=True,blank=True)
    favorite_count=models.PositiveIntegerField(default=0)
    youtube_id=models.CharField(max_length=12, null=True,blank=True)
    loading_time=models.DateTimeField(default=datetime.now)
    def increment_favorite_count(self):
        self.favorite_count += 1
        self.save(update_fields=['favorite_count'])

    def decrement_favorite_count(self):
        if self.favorite_count > 0:
            self.favorite_count -= 1
            self.save(update_fields=['favorite_count'])

    def __str__(self):
        return self.id
    
    class Meta:
        ordering = ['-loading_time']  #

    

