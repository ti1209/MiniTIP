from django.db.models import Q, Count, FloatField, IntegerField, Case, When, F
from django.db.models.functions import Cast
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from device import serializers
from device.models import Device, MACAddress
from policy.models import Policy
from tenant.models import Tenant
from zone.models import Zone
from django.db.models import Q, Count
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import timedelta


# ViewSets define the view behavior.
class DeviceDashboardViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.DeviceSerializer
    queryset = Device.objects.all()

    @action(detail=False, methods=['GET'], name='daily_chart')
    def daily_chart(self, request):
        today = timezone.localdate()

        year = Q(date_first_registered__year=today.year)
        month = Q(date_first_registered__month=today.month)
        day = Q(date_first_registered__day=today.day)

        today_count = Device.objects.filter(year & month & day).count()

        daily_count = list()
        daily_datetime = list()

        for num in range(30):
            day = today - timedelta(days=num)
            daily_datetime.append(day)

        for dfr in daily_datetime:
            year_q = Q(date_first_registered__year=dfr.year)
            month_q = Q(date_first_registered__month=dfr.month)
            day_q = Q(date_first_registered__day=dfr.day)

            daily_count.append(Device.objects.filter(year_q & month_q & day_q).count())

        return Response({
            'today_count': today_count,
            'daily_count': daily_count
        })

    @action(detail=False, methods=['GET'], name='statistics_per_period')
    def statistics_per_period(self, request):
        daily_count = list()
        monthly_count = list()

        daily_datetime = list()
        weekly_datetime = list()
        monthly_datetime = list()

        monthly_sum = 0
        weekly_sum = 0
        daily_sum = 0

        today = timezone.localdate()

        for num in range(30):
            day = today - timedelta(days=num)
            daily_datetime.append(day)

        for num in range(7):
            day = today - timedelta(days=num)
            weekly_datetime.append(day)

        for num in range(12):
            month = today - relativedelta(months=num)
            monthly_datetime.append(month)

        daily_datetime.reverse()
        weekly_datetime.reverse()
        monthly_datetime.reverse()

        total_sum = Device.objects.count()

        for day in daily_datetime:
            year_q = Q(date_first_registered__year=day.year)
            month_q = Q(date_first_registered__month=day.month)
            day_q = Q(date_first_registered__day=day.day)

            daily_count.append(Device.objects.filter(year_q & month_q & day_q).count())
            daily_sum += Device.objects.filter(year_q & month_q & day_q).count()

        for day in weekly_datetime:
            year_q = Q(date_first_registered__year=day.year)
            month_q = Q(date_first_registered__month=day.month)
            day_q = Q(date_first_registered__day=day.day)

            weekly_sum += Device.objects.filter(year_q & month_q & day_q).count()

        for month in monthly_datetime:
            year_q = Q(date_first_registered__year=month.year)
            month_q = Q(date_first_registered__month=month.month)

            monthly_count.append(Device.objects.filter(year_q & month_q).count())
            monthly_sum += Device.objects.filter(year_q & month_q).count()

        daily_average = daily_sum / 30
        weekly_average = weekly_sum / 7
        monthly_average = monthly_sum / 365

        return Response({
            'daily_average': int(daily_average),
            'total_sum': total_sum,
            'weekly_average': int(weekly_average),
            'weekly_sum': weekly_sum,
            'monthly_average': int(monthly_average),
            'monthly_sum': monthly_sum
        })

    @action(detail=False, methods=['GET'], name='policy_applied_status')
    def policy_applied_status(self, request):
        non_default = Device.objects.exclude(policy__policy_name='Default').count()
        total = Device.objects.count()

        non_default_rate = int(non_default / total * 100)

        return Response({
            'non_default': non_default,
            'total': total,
            'non_default_rate': non_default_rate
        })

    @action(detail=False, methods=['GET'], name='monthly_chart')
    def monthly_chart(self, request):
        today = timezone.localdate()

        monthly_datetime = list()
        monthly_count = list()

        for num in range(12):
            month = today - relativedelta(months=num)
            monthly_datetime.append(month)

        for dfr in monthly_datetime:
            year_q = Q(date_first_registered__year=dfr.year)
            month_q = Q(date_first_registered__month=dfr.month)

            monthly_count.append(Device.objects.filter(year_q & month_q).count())

        return Response({
            'monthly_count': monthly_count
        })

    @action(detail=False, methods=['GET'], name='os_version_list')
    def os_version_list(self, request):
        total = Device.objects.count()

        windows_count = Device.objects.filter(Q(os_version__startswith='Microsoft') |
                                              Q(os_version__startswith='Win32NT')).count()
        mac_count = Device.objects.filter(os_version__startswith='macOS').count()
        linux_count = Device.objects.filter(Q(os_version__startswith='Red Hat') |
                                            Q(os_version__startswith='Amazon') |
                                            Q(os_version__startswith='CentOS') |
                                            Q(os_version__startswith='Ubuntu')).count()
        unknown_count = total - windows_count - mac_count - linux_count

        return Response({
            'windows_count': windows_count,
            'macOS_count': mac_count,
            'linux_count': linux_count,
            'unknown_count': unknown_count
        })

    @action(detail=False, methods=['GET'], name='license_valid_status')
    def license_valid_status(self, request):
        f = Q()

        today = timezone.localdate()
        before_ninety_day = today - timedelta(days=90)

        total = Device.objects.count()

        mac_address = MACAddress.objects.values_list('mac_address', flat=True)\
            .annotate(count=Count('mac_address')) \
            .filter(count__gt=1)

        for i in range(mac_address.count()):
            f |= Q(macaddress__mac_address=mac_address[i])

        invalid = (Device.objects.filter(f).annotate(count=Count('id')) |
                   Device.objects.filter(date_offline__lte=before_ninety_day)).count()
        valid = total - invalid

        return Response({
            'invalid': invalid,
            'valid': valid
        })

    @action(detail=False, methods=['GET'], name='version_update_status')
    def version_update_status(self, request):
        update_count = Device.objects.filter(agent_version='2.1.1550').count()
        outdated_count = Device.objects.exclude(agent_version='2.1.1550').count()

        return Response({
            'update_count': update_count,
            'outdated_count': outdated_count
        })

    @action(detail=False, methods=['GET'], name='device_active_status')
    def device_active_status(self, request):
        today = timezone.localdate()

        before_thirty_day = today - timedelta(days=30)
        before_ninety_day = today - timedelta(days=90)

        total = Device.objects.count()

        online = (Device.objects.filter(state='Online').count() / total) * 100

        before_thirty_total = Device.objects.filter(date_offline__lte=before_thirty_day)\
            .filter(date_offline__gt=before_ninety_day).count()
        before_ninety_total = Device.objects.filter(date_offline__lte=before_ninety_day).count()

        before_thirty_days = (before_thirty_total / total) * 100
        before_ninety_days = (before_ninety_total / total) * 100

        return Response({
            'online': int(online),
            'thirty': int(before_thirty_days),
            'ninety': int(before_ninety_days)
        })

    @action(detail=False, methods=['GET'], name='os_count_per_tenant')
    def os_count_per_tenant(self, request):
        self.queryset = Tenant.objects.annotate(
            windows_count=Count('device', filter=Q(device__os_version__startswith='Microsoft')
                                                 | Q(device__os_version__startswith='Win32NT'))) \
                       .annotate(mac_count=Count('device', filter=Q(device__os_version__startswith='macOS'))) \
                       .annotate(linux_count=Count('device', filter=Q(device__os_version__startswith='Red Hat')
                                                                    | Q(device__os_version__startswith='Amazon')
                                                                    | Q(device__os_version__startswith='CentOS')
                                                                    | Q(device__os_version__startswith='Ubuntu')))[:10]

        self.serializer_class = serializers.OSCountPerTenantSerializer

        return super(DeviceDashboardViewset, self).list(request)

    @action(detail=False, methods=['GET'], name='device_per_policy_per_tenant')
    def device_per_policy_per_tenant(self, request):
        self.queryset = Policy.objects.annotate(count=Count('tenant'))[:10]
        self.serializer_class = serializers.DevicePerPolicyPerTenantSerializer

        return super(DeviceDashboardViewset, self).list(request)

    @action(detail=False, methods=['GET'], name='over_ninety_days')
    def over_ninety_days(self, request):
        today = timezone.localdate()
        ninety_day = today - timedelta(days=90)

        self.queryset = Device.objects.filter(date_offline__lte=ninety_day)[:10]
        self.serializer_class = serializers.DeletableDeviceSerializer

        return super(DeviceDashboardViewset, self).list(request)

    @action(detail=False, methods=['GET'], name='duplicated_mac_address')
    def duplicated_mac_address(self, request):
        f = Q()

        address = MACAddress.objects.values_list('mac_address', flat=True) \
            .annotate(count=Count('mac_address')) \
            .filter(count__gt=1)

        for i in range(address.count()):
            f |= Q(macaddress__mac_address=address[i])

        self.queryset = Device.objects.filter(f).annotate(count=Count('id'))[:10]
        self.serializer_class = serializers.DeletableDeviceSerializer

        return super(DeviceDashboardViewset, self).list(request)

    @action(detail=False, methods=['GET'], name='agent_version_per_tenant')
    def agent_version_per_tenant(self, request):
        self.queryset = Tenant.objects.annotate(fourty_count=Count('device', filter=Q(device__agent_version='2.0.1540')))
        self.queryset = self.queryset.annotate(
            thirtyfour_count=Count('device', filter=Q(device__agent_version='2.0.1534')))
        self.queryset = self.queryset.annotate(thirty_count=Count('device', filter=Q(device__agent_version='2.0.1530')))
        self.queryset = self.queryset.annotate(twenty_count=Count('device', filter=Q(device__agent_version='2.0.1520')))
        self.queryset = self.queryset.annotate(
            unupdate_count=Count('device', filter=~Q(device__agent_version='2.1.1550')))

        self.queryset = self.queryset.annotate(
            update_count=Count('device', filter=Q(device__agent_version='2.1.1550'))) \
                            .annotate(td_total=Count('device')) \
                            .annotate(rate=Case(When(
            condition=Q(td_total__gt=0),
            then=Cast(
                (Cast(F('update_count'), FloatField()) /
                 Cast(F('td_total'), FloatField()) * 100.0),
                IntegerField()
            )
        ), default=0)
        )[:10]
        self.serializer_class = serializers.AgentVersionPerTenantSerializer

        return super(DeviceDashboardViewset, self).list(request)
