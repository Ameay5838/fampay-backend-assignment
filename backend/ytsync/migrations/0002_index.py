from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_searchvector(apps, schema_editor):
    VideoListing = apps.get_model("ytsync", "VideoListing")
    VideoListing.objects.update(searchvector=SearchVector("title", "description"))


class Migration(migrations.Migration):

    dependencies = [
        ("ytsync", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER searchvector_trigger
            BEFORE INSERT OR UPDATE OF title, description, searchvector
            ON ytsync_videolisting
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                searchvector, 'pg_catalog.english', title, description
            );
            UPDATE ytsync_videolisting SET searchvector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS searchvector_trigger
            ON ytsync_videolisting;
            """,
        ),
        migrations.RunPython(
            compute_searchvector, reverse_code=migrations.RunPython.noop
        ),
    ]
