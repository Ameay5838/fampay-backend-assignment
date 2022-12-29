from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_search_vector(apps, schema_editor):
    VideoListing = apps.get_model("ytsync", "VideoListing")
    VideoListing.objects.update(search_vector=SearchVector("title", "description"))


class Migration(migrations.Migration):

    dependencies = [
        ("ytsync", "0002_videolisting_ytsync_vide_publish_223d29_idx"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER search_vector_trigger
            BEFORE INSERT OR UPDATE OF title, description, search_vector
            ON ytsync_videolisting
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                search_vector, 'pg_catalog.english', title, description
            );
            UPDATE ytsync_videolisting SET search_vector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS search_vector_trigger
            ON ytsync_videolisting;
            """,
        ),
        migrations.RunPython(
            compute_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]
