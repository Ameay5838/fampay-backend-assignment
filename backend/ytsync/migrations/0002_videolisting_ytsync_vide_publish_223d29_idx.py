# Generated by Django 4.1.4 on 2022-12-29 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ytsync', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='videolisting',
            index=models.Index(fields=['publishedAt'], name='ytsync_vide_publish_223d29_idx'),
        ),
    ]
