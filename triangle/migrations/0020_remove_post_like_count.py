# Generated by Django 2.1.5 on 2019-03-27 23:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('triangle', '0019_post_like_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='like_count',
        ),
    ]
