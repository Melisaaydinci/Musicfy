# Generated by Django 5.0 on 2024-05-14 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0006_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='favorite_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
