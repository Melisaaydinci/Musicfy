
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from music.models import Music


class CustomUser(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    phone_number=models.CharField(max_length=11,null=True,unique=True)
    email=models.EmailField(null=True,unique=True)
    favorites = models.ManyToManyField(Music, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

@receiver(pre_delete, sender=CustomUser)
def remove_favorites_on_customer_delete(sender, instance, **kwargs):
    instance = CustomUser.objects.get(id=instance.id)
    for music in instance.favorites.all():
        music.decrement_favorite_count()