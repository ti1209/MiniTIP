# from django.db import models
#
#
# # Create your models here.
# class Device(models.Model):
#     threat = models.ManyToManyField(to="Threat.Threat", through='DeviceThreat')
#     tenant = models.ForeignKey(to="Tenant.Tenant", on_delete=models.CASCADE)
#     policy = models.ForeignKey(to="Policy.Policy", on_delete=models.CASCADE)
#
#     de_num = models.CharField(max_length=100)
#     name = models.CharField(max_length=100, null=True)
#     state = models.CharField(max_length=10, null=True)
#     agent_version = models.CharField(max_length=20, null=True)
#     date_first_registered = models.DateTimeField()
#     ip_addresses = models.CharField(max_length=100, null=True)
#     mac_addresses = models.CharField(max_length=100, null=True)
#
#
# class DeviceThreat(models.Model):
#     threat = models.ForeignKey(to="Threat.Threat", on_delete=models.CASCADE)
#     device = models.ForeignKey(to="Device.Device", on_delete=models.CASCADE)
#     datetime = models.DateTimeField()
#     file_status = models.CharField(max_length=15, null=True)
#     path = models.TextField(null=True)
from django.db import models


class Device(models.Model):
    # Relation Key Declaration
    tenant = models.ForeignKey(
        to="tenant.Tenant",
        on_delete=models.CASCADE
    )

    policy = models.ForeignKey(
        to="policy.Policy",
        on_delete=models.SET_NULL, null=True
    )

    zone = models.ManyToManyField(
        to="zone.Zone",
        through="device.ZoneDevices"
    )

    # devices API's Return Values
    device_id = models.CharField(
        max_length=36,
        null=True
    )

    name = models.CharField(
        max_length=200,
        null=True
    )

    state = models.CharField(
        max_length=10,
        null=True
    )

    agent_version = models.CharField(
        max_length=10,
        null=True
    )

    date_first_registered = models.DateTimeField(
        verbose_name='First Registered Date',
        null=True
    )

    # device API's Return Values
    host_name = models.CharField(
        max_length=200,
        null=True
    )

    os_version = models.CharField(
        max_length=200,
        null=True
    )

    last_logged_in_user = models.CharField(
        max_length=200,
        null=True
    )

    update_type = models.CharField(
        max_length=50,
        null=True
    )

    update_available = models.BooleanField(
        null=True
    )

    background_detection = models.BooleanField(
        null=True
    )

    is_safe = models.BooleanField(
        null=True
    )

    date_offline = models.DateTimeField(
        verbose_name='Offline Date',
        null=True
    )

    date_last_modified = models.DateTimeField(
        verbose_name='Last Modified Date',
        null=True
    )

    sync_uuid = models.CharField(
        max_length=36,
        null=True
    )

    def __str__(self):
        return self.name


class IPAddress(models.Model):
    device = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE,
    )

    ip_address = models.CharField(
        max_length=50,
        null=True,
    )

    def __str__(self):
        return self.ip_address


class MACAddress(models.Model):
    device = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE
    )

    mac_address = models.CharField(
        max_length=50,
        null=True
    )

    def __str__(self):
        return self.mac_address


class ZoneDevices(models.Model):
    tenant = models.ForeignKey(
        to="tenant.Tenant",
        on_delete=models.CASCADE
    )

    device = models.ForeignKey(
        to="device.Device",
        on_delete=models.CASCADE
    )

    zone = models.ForeignKey(
        to="zone.Zone",
        on_delete=models.CASCADE
    )

    sync_uuid = models.CharField(
        max_length=36,
        null=True
    )

    def __str__(self):
        return self.zone.zone_name

