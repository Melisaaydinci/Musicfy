# Generated by Django 5.0 on 2024-05-05 23:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('music', '0005_remove_musiclistening_music_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('release', models.CharField(max_length=200)),
                ('artist_name', models.CharField(max_length=200)),
                ('year', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MusicListening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listen_count', models.IntegerField(blank=True, null=True)),
                ('listener', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listener', to=settings.AUTH_USER_MODEL)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music', to='music.music')),
            ],
        ),
    ]