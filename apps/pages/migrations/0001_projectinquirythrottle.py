from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProjectInquiryThrottle",
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
                ("bucket_key", models.CharField(max_length=64, unique=True)),
                ("attempt_count", models.PositiveIntegerField(default=1)),
                ("expires_at", models.DateTimeField(db_index=True)),
            ],
            options={"db_table": "apps_pages_projectinquirythrottle"},
        ),
    ]
