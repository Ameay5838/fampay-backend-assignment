# Generated by Django 4.1.4 on 2022-12-28 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VideoListing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("video_id", models.CharField(max_length=100, unique=True)),
                ("title", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=100)),
                ("publishedAt", models.DateTimeField()),
                ("thumbnailUrls", models.JSONField()),
            ],
            options={
                "ordering": ["-publishedAt"],
            },
        ),
        migrations.AddIndex(
            model_name="videolisting",
            index=models.Index(fields=["title"], name="ytsync_vide_title_163afe_idx"),
        ),
    ]