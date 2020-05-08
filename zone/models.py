# from django.db import models
#
#
# # Create your models here.
# class Zone(models.Model):
#     tenant = models.ForeignKey(to="Tenant.Tenant", on_delete=models.CASCADE)
#     policy = models.ForeignKey(to="Policy.Policy", on_delete=models.CASCADE)
#     device = models.ManyToManyField(to="Device.Device")
#
#     zo_num = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     criticality = models.CharField(max_length=10, choices=[('Low', 'Low'),
#                                                            ('Normal', 'Normal'),
#                                                            ('High', 'High')])
#     update_type = models.CharField(max_length=10, choices=[('Production', 'Production'),
#                                                            ('Pilot', 'Pilot'),
#                                                            ('Test', 'Test')])
#     zone_rule_id = models.CharField(max_length=100, null=True)
#     date_created = models.DateTimeField()
#     date_modified = models.DateTimeField()
from django.db import models


class Zone(models.Model):
    tenant = models.ForeignKey(
        to="tenant.Tenant",
        on_delete=models.CASCADE
    )

    policy = models.ForeignKey(
        to="policy.Policy",
        on_delete=models.SET_NULL,
        null=True
    )

    zone_id = models.CharField(
        max_length=36,
        null=True
    )

    zone_name = models.CharField(
        max_length=255,
        null=True
    )

    criticality = models.CharField(
        max_length=20,
        null=True
    )

    zone_rule_id = models.CharField(
        max_length=50,
        null=True
    )

    update_type = models.CharField(
        max_length=50,
        null=True
    )

    date_modified = models.DateTimeField(
        verbose_name='Modified Date',
        null=True
    )

    date_created = models.DateTimeField(
        verbose_name='Created Date',
        null=True
    )

    sync_uuid = models.CharField(
        max_length=36,
        null=True
    )

    def __str__(self):
        return self.zone_name
