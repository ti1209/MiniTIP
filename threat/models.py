# from django.db import models
#
#
# # Create your models here.
# class Threat(models.Model):
#     tenant = models.ForeignKey(to="Tenant.Tenant", on_delete=models.CASCADE)
#
#     name = models.CharField(max_length=150)
#     sha256 = models.CharField(max_length=70)
#     md5 = models.CharField(max_length=40, null=True)
#     cylance_score = models.FloatField(null=True)
#     av_industry = models.CharField(max_length=10, null=True)
#     classification = models.CharField(max_length=20, blank=True)
#     sub_classification = models.CharField(max_length=20, blank=True)
#     Global_Quarantined = models.BooleanField()
#     safelisted = models.BooleanField()
#     file_size = models.IntegerField()
#     unique_to_cylance = models.BooleanField()
#     last_found = models.DateTimeField()
from datetime import datetime

from django.db import models
from django.utils import timezone


class Threat(models.Model):
    classification_choices = (
        ('Malware', u'Malware'),
        ('PUP', u'PUP')
    )

    # Relation Key Declaration
    tenant = models.ForeignKey(
        to="tenant.Tenant",
        on_delete=models.CASCADE
    )

    device = models.ManyToManyField(
        "device.Device",
        through='threat.ThreatDevices'
    )

    globallist = models.OneToOneField(
        "globallist.GlobalList",
        on_delete=models.SET_NULL,
        null=True
    )

    # Threats API's Return Field
    sha256 = models.CharField(
        max_length=64)

    name = models.CharField(
        max_length=500,
        null=True
    )

    md5 = models.CharField(
        max_length=32,
        null=True
    )

    cylance_score = models.IntegerField(
        null=True
    )

    classification = models.CharField(
        max_length=20,
        choices=classification_choices,
        null=True
    )

    sub_classification = models.CharField(
        max_length=20,
        null=True
    )

    global_quarantined = models.BooleanField(
        null=True
    )

    safelisted = models.BooleanField(
        null=True
    )

    file_size = models.IntegerField(
        null=True
    )

    unique_to_cylance = models.BooleanField(
        null=True
    )

    last_found = models.DateTimeField(
        verbose_name='Last found date',
        default=datetime(1970, 1, 1, tzinfo=timezone.utc),
        null=True
    )

    first_found = models.DateTimeField(
        verbose_name='First found date',
        null=True
    )

    # Threat API's Return Field
    signed = models.BooleanField(
        null=True
    )

    cert_publisher = models.CharField(
        max_length=10000,
        null=True
    )

    cert_issuer = models.CharField(
        max_length=10000,
        null=True
    )

    cert_timestamp = models.DateTimeField(
        verbose_name='Certification Date',
        null=True
    )

    running = models.BooleanField(
        null=True
    )

    auto_run = models.BooleanField(
        null=True
    )

    detected_by = models.CharField(
        max_length=200,
        null=True
    )

    # Threat Custom Field
    updated = models.BooleanField(
        null=True
    )

    deleted = models.BooleanField(
        null=True
    )

    sync_uuid = models.CharField(
        max_length=36,
        null=True
    )

    def __str__(self):
        return self.sha256


# Threat-Devices intermediate Model
class ThreatDevices(models.Model):
    # Relation Key Declaration
    tenant = models.ForeignKey(
        to="tenant.Tenant",
        on_delete=models.CASCADE
    )

    device = models.ForeignKey(
        to="device.Device",
        on_delete=models.CASCADE
    )

    threat = models.ForeignKey(
        to="threat.Threat",
        on_delete=models.CASCADE
    )

    # Expanded Field
    date_found = models.DateTimeField(
        null=True
    )

    file_status = models.CharField(
        max_length=15,
        null=True
    )

    file_path = models.CharField(
        max_length=10000,
        null=True
    )

    sync_uuid = models.CharField(
        max_length=36,
        null=True
    )
