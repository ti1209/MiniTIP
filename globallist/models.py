# from django.db import models
#
#
# # Create your models here.
# class GlobalList(models.Model):
#     tenant = models.ForeignKey(to="tenant.Tenant", on_delete=models.CASCADE)
#
#     name = models.CharField(max_length=255)
#     sha256 = models.CharField(max_length=70)
#     md5 = models.CharField(max_length=40, null=True)
#     cylance_score = models.FloatField(null=True)
#     av_industry = models.CharField(max_length=10, null=True)
#     classification = models.CharField(max_length=20, blank=True)
#     sub_classification = models.CharField(max_length=20, blank=True)
#     list_type = models.CharField(max_length=20, null=True)
#     category = models.CharField(max_length=30, blank=True, default="")
#     added = models.DateTimeField()
#
#     # todo cylance user app 추가 시 추후 연결
#     added_by = models.CharField(max_length=100, default="NONE")
#     reason = models.CharField(max_length=100, default="NONE")
from django.db import models


class GlobalList(models.Model):
    # Choices lists Declaration
    list_type_choices = (
        ('GlobalQuarantine', u'GlobalQuarantine'),
        ('GlobalSafe', u'GlobalSafe')
    )
    classification_choices = (
        ('Malware', u'Malware'),
        ('PUP', u'PUP')
    )
    # Relation Key Declaration
    tenant = models.ForeignKey(
        to="tenant.Tenant",
        on_delete=models.CASCADE
    )
    # added_by = models.ForeignKey(
    #     to="user.CylanceUser",
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
    # Field Declaration
    sha256 = models.CharField(
        max_length=64,
        null=True
    )
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
    av_industry = models.IntegerField(
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
    list_type = models.CharField(
        max_length=16,
        choices=list_type_choices,
        null=True
    )
    category = models.CharField(
        max_length=50,
        null=True
    )
    added = models.DateTimeField(
        'Added Time',
        null=True
    )
    reason = models.CharField(
        max_length=200,
        null=True
    )
    sync_uuid = models.CharField(
        max_length=36,
        null=True
    )

    def __str__(self):
        return self.sha256
