from django.db import models


# Create your models here.
class Policy(models.Model):
    tenant = models.ForeignKey(
        "tenant.Tenant",
        on_delete=models.CASCADE
    )
    policy_id = models.CharField(
        max_length=36
    )
    policy_name = models.CharField(
        max_length=200,
        null=True
    )
    policy_utctimestamp = models.DateTimeField(
        'Time Stamp',
        null=True
    )
    policy_checksum = models.CharField(
        max_length=32,
        null=True
    )
    sync_uuid = models.CharField(
        max_length=36,
        null=True
    )
    date_added = models.DateTimeField(
        'Added Date',
        null=True
    )
    date_modified = models.DateTimeField(
        'Modified Date',
        null=True
    )
    device_count = models.IntegerField(
        null=True
    )
    zone_count = models.IntegerField(
        null=True
    )

    def __str__(self):
        return self.policy_name
