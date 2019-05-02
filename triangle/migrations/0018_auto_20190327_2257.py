# Generated by Django 2.1.5 on 2019-03-27 22:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triangle', '0017_remove_post_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='posts_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
