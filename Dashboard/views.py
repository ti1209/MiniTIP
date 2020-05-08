from django.shortcuts import render
from policy.models import Policy
from tenant.models import Tenant
from device.models import Device, MACAddress
from globallist.models import GlobalList
from django.db.models import Q, Count, FloatField, IntegerField, Case, When, F
from django.db.models.functions import Cast
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import timedelta


# Create your views here.
def threat(request):
    return render(request, 'TIP/threat.html')


def device(request):
    daily_count = list()
    monthly_count = list()

    daily_datetime = list()
    monthly_datetime = list()

    monthly_sum = 0
    weekly_sum = 0
    daily_sum = 0

    today = timezone.localdate()

    year = Q(date_first_registered__year=today.year)
    month = Q(date_first_registered__month=today.month)
    day = Q(date_first_registered__day=today.day)

    today_count = Device.objects.filter(year & month & day).count()

    total = Device.objects.count()

    for dm in range(12):
        m = today - relativedelta(months=dm)
        monthly_datetime.append(m)

    for dd in range(30):
        d = today - timedelta(days=dd)
        daily_datetime.append(d)

    daily_datetime.reverse()
    monthly_datetime.reverse()

    num = 0

    thirty_day = today - timedelta(days=30)
    ninety_day = today - timedelta(days=90)

    thirty_total = Device.objects.filter(date_offline__lte=thirty_day).filter(date_offline__gt=ninety_day).count()
    ninety_total = Device.objects.filter(date_offline__lte=ninety_day).count()

    thirty_days = (thirty_total / total) * 100
    ninety_days = (ninety_total / total) * 100

    for d in daily_datetime:
        year_q = Q(date_first_registered__year=d.year)
        month_q = Q(date_first_registered__month=d.month)
        day_q = Q(date_first_registered__day=d.day)

        daily_count.append(Device.objects.filter(year_q & month_q & day_q).count())
        daily_sum += Device.objects.filter(year_q & month_q & day_q).count()

        if num < 7:
            weekly_sum += Device.objects.filter(year_q & month_q & day_q).count()

        num += 1

    weekly_average = weekly_sum / 7
    daily_average = daily_sum / 30

    for dt in monthly_datetime:
        year_q = Q(date_first_registered__year=dt.year)
        month_q = Q(date_first_registered__month=dt.month)
        monthly_count.append(Device.objects.filter(year_q & month_q).count())
        monthly_sum += Device.objects.filter(year_q & month_q).count()

    monthly_average = monthly_sum / 365

    windows = Device.objects.filter(Q(os_version__startswith='Microsoft') | Q(os_version__startswith='Win32NT'))
    mac = Device.objects.filter(os_version__startswith='macOS')
    linux = Device.objects.filter(Q(os_version__startswith='Red Hat') | Q(os_version__startswith='Amazon') |
                                  Q(os_version__startswith='CentOS') | Q(os_version__startswith='Ubuntu'))

    update = Device.objects.filter(agent_version='2.1.1550').count()
    unupdate = total - update

    online = (Device.objects.filter(state='Online').count() / total) * 100

    address = MACAddress.objects.values_list('mac_address', flat=True) \
        .annotate(count=Count('mac_address')) \
        .filter(count__gt=1)

    f = Q()

    for i in range(address.count()):
        f |= Q(macaddress__mac_address=address[i])

    invalid = (Device.objects.filter(f).annotate(count=Count('id')) |
               Device.objects.filter(date_offline__lte=ninety_day)).count()

    non_default = Device.objects.exclude(policy__policy_name='Default').count()

    over_ninety_days = Device.objects.filter(date_offline__lte=ninety_day)[:10]
    mac_duplicate = Device.objects.filter(f).annotate(count=Count('id'))[:10]

    os_count = Tenant.objects.annotate(windows_count=Count('device', filter=Q(device__os_version__startswith='Microsoft')
                                                                          | Q(device__os_version__startswith='Win32NT')))\
        .annotate(mac_count=Count('device', filter=Q(device__os_version__startswith='macOS')))\
        .annotate(linux_count=Count('device', filter=Q(device__os_version__startswith='Red Hat')
                                                                          | Q(device__os_version__startswith='Amazon')
                                                                          | Q(device__os_version__startswith='CentOS')
                                                                          | Q(device__os_version__startswith='Ubuntu')))[:10]

    policy_per_tenant = Policy.objects.annotate(count=Count('tenant'))[:10]

    unupdate_count = Tenant.objects.annotate(
        unupdate_count=Count('device', filter=~Q(device__agent_version='2.1.1550')))

    fourty_count = Tenant.objects.annotate(fourty_count=Count('device', filter=Q(device__agent_version='2.0.1540')))
    thirtyfour_count = Tenant.objects.annotate(thirtyfour_count=Count('device', filter=Q(device__agent_version='2.0.1534')))
    thirty_count = Tenant.objects.annotate(thirty_count=Count('device', filter=Q(device__agent_version='2.0.1530')))
    twenty_count = Tenant.objects.annotate(twenty_count=Count('device', filter=Q(device__agent_version='2.0.1520')))

    rate = Tenant.objects.annotate(update_count=Count('device', filter=Q(device__agent_version='2.1.1550')))\
        .annotate(td_total=Count('device'))\
        .annotate(rate=Case(
            When(
                condition=Q(td_total__gt=0),
                then=Cast(
                    (Cast(F('update_count'), FloatField()) /
                     Cast(F('td_total'), FloatField()) * 100.0),
                    IntegerField()
                )
            ),
            default=0
        )
    )[:10]

    # rate = list()
    #
    # for d in Tenant.objects.all():
    #     di = dict()
    #     di['tenant_id'] = d.id
    #     try:
    #         di['rate'] = int((Device.objects.filter(Q(agent_version='2.1.1550') & Q(tenant_id=d.id)).count() /
    #                           Device.objects.filter(tenant_id=d.id).count()) * 100)
    #     except ZeroDivisionError:
    #         di['rate'] = 0
    #     rate.append(di)

    return render(
        request,
        'TIP/device.html',
        # context={
        #     "daily_count": daily_count,
        #     "today_count": today_count,
        #
        #     "daily_average": int(daily_average),
        #     "total": total,
        #     "weekly_average": int(weekly_average),
        #     "weekly_sum": weekly_sum,
        #     "monthly_average": int(monthly_average),
        #     "monthly_sum": monthly_sum,
        #
        #     "non_default": non_default,
        #     "non_default_rate": int(non_default / total * 100),
        #
        #     "monthly_count": monthly_count,
        #
        #     "windows": windows.count(),
        #     "mac": mac.count(),
        #     "linux": linux.count(),
        #     "unknown": total - windows.count() - mac.count() - linux.count(),
        #
        #     "invalid": invalid,
        #     "rest": total - invalid,
        #
        #     "update": update,
        #     "unupdate": unupdate,
        #
        #     "online": int(online),
        #     "thirty": int(thirty_days),
        #     "ninety": int(ninety_days),
        #
        #     "os_count": os_count,
        #
        #     "policy_per_tenant": policy_per_tenant,
        #
        #     "over_ninety_days": over_ninety_days,
        #     "mac_duplicate": mac_duplicate,
        #
        #     "rate": rate,
        #     "unupdate_count": unupdate_count,
        #     "fourty_count": fourty_count,
        #     "thirtyfour_count": thirtyfour_count,
        #     "thirty_count": thirty_count,
        #     "twenty_count": twenty_count
        # }
    )


def globalist(request):
    daily_malware_count = list()
    daily_pup_count = list()
    daily_safe_count = list()

    malware_monthly_count = list()
    pup_monthly_count = list()
    safe_monthly_count = list()

    month_datetime = list()
    day_datetime = list()

    malware_sum = 0
    pup_sum = 0
    safe_sum = 0

    today = timezone.localdate()

    for gm in range(12):
        dm = today - relativedelta(months=gm)
        month_datetime.append(dm)

    for gd in range(30):
        dl = today - timedelta(days=gd)
        day_datetime.append(dl)

    month_datetime.reverse()
    day_datetime.reverse()

    year = Q(added__year=today.year)
    month = Q(added__month=today.month)
    day = Q(added__day=today.day)

    malware = (Q(reason__icontains='멀웨어 - ') | Q(reason__icontains='Mal - '))
    pup = Q(reason__icontains='PUP - ')
    safe = Q(list_type='GlobalSafe')

    # 오늘자 데이터
    today_malware_count = GlobalList.objects.filter(year & month & day & malware).count()
    today_pup_count = GlobalList.objects.filter(year & month & day & pup).count()
    today_safe_count = GlobalList.objects.filter(year & month & day & safe).count()

    # 월별 데이터
    for month in month_datetime:
        year_q = Q(added__year=month.year)
        month_q = Q(added__month=month.month)

        malware_monthly_count.append(GlobalList.objects.filter(year_q & month_q & malware).count())
        pup_monthly_count.append(GlobalList.objects.filter(year_q & month_q & pup).count())
        safe_monthly_count.append(GlobalList.objects.filter(year_q & month_q & safe).count())

    # 일별 데이터
    for daily in day_datetime:
        year_q = Q(added__year=daily.year)
        month_q = Q(added__month=daily.month)
        day_q = Q(added__day=daily.day)

        daily_malware_count.append(GlobalList.objects.filter(year_q & month_q & day_q & malware).count())
        daily_pup_count.append(GlobalList.objects.filter(year_q & month_q & day_q & pup).count())
        daily_safe_count.append(GlobalList.objects.filter(year_q & month_q & day_q & safe).count())

        malware_sum += GlobalList.objects.filter(year_q & month_q & day_q & malware).count()
        pup_sum += GlobalList.objects.filter(year_q & month_q & day_q & pup).count()
        safe_sum += GlobalList.objects.filter(year_q & month_q & day_q & safe).count()

    # 누적 데이터
    malware_total = GlobalList.objects.filter(malware).count()
    pup_total = GlobalList.objects.filter(pup).count()
    safe_total = GlobalList.objects.filter(safe).count()

    # 하루 평균 데이터
    malware_avg = malware_sum / 30
    pup_avg = pup_sum / 30
    safe_avg = safe_sum / 30

    return render(
        request,
        'TIP/globalist.html',
        context={
            "today_malware_count": today_malware_count,
            "today_pup_count": today_pup_count,
            "today_safe_count": today_safe_count,

            "daily_malware_count": daily_malware_count,
            "daily_pup_count": daily_pup_count,
            "daily_safe_count": daily_safe_count,

            "malware_monthly_count": malware_monthly_count,
            "pup_monthly_count": pup_monthly_count,
            "safe_monthly_count": safe_monthly_count,

            "malware_avg": int(malware_avg),
            "pup_avg": int(pup_avg),
            "safe_avg": int(safe_avg),

            "malware_total": malware_total,
            "pup_total": pup_total,
            "safe_total": safe_total
        }
    )
