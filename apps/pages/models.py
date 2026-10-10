from django.db import models


class ProjectInquiryThrottle(models.Model):
    bucket_key = models.CharField(max_length=64, unique=True)
    attempt_count = models.PositiveIntegerField(default=1)
    expires_at = models.DateTimeField(db_index=True)

    class Meta:
        db_table = "apps_pages_projectinquirythrottle"
