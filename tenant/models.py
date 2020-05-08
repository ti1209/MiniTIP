from django.db import models


# Create your models here.
class Customer(models.Model):
    customer_name = models.CharField(
        max_length=50,
    )
    current_agent_version = models.CharField(
        max_length=10,
        null=True
    )
    license_count = models.IntegerField(
        null=True
    )
    date_started_license = models.DateTimeField(
        verbose_name='License Started Date',
        null=True
    )
    date_expire_license = models.DateTimeField(
        verbose_name='License Expire Date',
        null=True
    )

    def __str__(self):
        return self.customer_name


class Tenant(models.Model):
    tenant_id = models.CharField(
        max_length=36
    )
    tenant_name = models.CharField(
        max_length=50
    )
    app_id = models.CharField(
        max_length=50,
        null=True
    )
    app_secret = models.CharField(
        max_length=50,
        null=True
    )
    date_sync = models.DateTimeField(
        'cylance sync date',
        null=True
    )
    customer = models.ForeignKey(
        'tenant.Customer',
        on_delete=models.CASCADE,
        related_name='tenants'
    )
    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.tenant_name


class TenantCount(models.Model):
    tenant = models.ForeignKey(
        to='tenant.Tenant',
        on_delete=models.CASCADE,
        related_name='counts'
    )
    device_count = models.IntegerField(
        null=True
    )
    defalut_policy_device_count = models.IntegerField(
        null=True
    )
    non_defalut_policy_device_count = models.IntegerField(
        null=True
    )
    threat_count = models.IntegerField(
        null=True
    )
    labelled_threat_count = models.IntegerField(
        null=True
    )
    unlabelled_threat_count = models.IntegerField(
        null=True
    )
