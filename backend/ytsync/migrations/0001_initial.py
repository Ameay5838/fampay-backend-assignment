# Generated by Django 4.1.4 on 2022-12-29 20:48

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('details', models.CharField(max_length=200, null=True)),
                ('key', models.TextField()),
                ('exhausted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='VideoListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoId', models.CharField(max_length=200, unique=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('publishedAt', models.DateTimeField()),
                ('thumbnailUrls', models.JSONField()),
                ('searchvector', django.contrib.postgres.search.SearchVectorField(null=True)),
            ],
            options={
                'ordering': ['-publishedAt'],
            },
        ),
        migrations.AddIndex(
            model_name='videolisting',
            index=models.Index(fields=['publishedAt'], name='ytsync_vide_publish_223d29_idx'),
        ),
        migrations.AddIndex(
            model_name='videolisting',
            index=django.contrib.postgres.indexes.GinIndex(fields=['searchvector'], name='ytsync_vide_searchv_13a8ce_gin'),
        ),
    ]
