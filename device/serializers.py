from rest_framework import serializers

from device.models import Device, IPAddress, MACAddress
from policy.models import Policy
from tenant.models import Tenant
from zone.models import Zone


# Serializers define the API representation.
class DeviceSerializer(serializers.ModelSerializer):
    # tenant_name = serializers.CharField(
    #     label='테넌트', source='tenant.tenant_name'
    # source를 사용하는 경우 = viewset에 정의 안한 경우
    # )

    name = serializers.CharField(
        label='name'
    )

    state = serializers.CharField(
        label='state'
    )

    os_version = serializers.CharField(
        label='os_version'
    )

    date_first_registered = serializers.DateTimeField(
        label='date_first_registered'
    )

    date_offline = serializers.DateTimeField(
        label='date_offline'
    )

    # 실제 정의하는 곳
    class Meta:
        model = Device
        fields = (
            'name',
            'state',
            'os_version',
            'date_first_registered',
            'date_offline'
        )


class OSCountPerTenantSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(
        label='tenant_name',
    )

    windows_count = serializers.IntegerField(
        label='windows_count'
    )

    mac_count = serializers.IntegerField(
        label='mac_count'
    )

    linux_count = serializers.IntegerField(
        label='linux_count'
    )

    # 실제 정의하는 곳
    class Meta:
        model = Tenant
        fields = (
            'tenant_name',
            'windows_count',
            'mac_count',
            'linux_count'
        )


class DevicePerPolicyPerTenantSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(
        label='tenant_name',
        source='tenant.tenant_name'
    )

    policy_name = serializers.CharField(
        label='policy_name'
    )

    device_count = serializers.IntegerField(
        label='device_count'
    )

    # 실제 정의하는 곳
    class Meta:
        model = Policy
        fields = (
            'tenant_name',
            'policy_name',
            'device_count'
        )


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        depth = 1
        fields = ('zone_name',)


class IPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPAddress
        depth = 1
        fields = ('ip_address',)


class MACSerializer(serializers.ModelSerializer):
    class Meta:
        model = MACAddress
        depth = 1
        fields = ('mac_address',)


class DeletableDeviceSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(
        label='tenant_name',
        source='tenant.tenant_name'
    )

    zone_name = ZoneSerializer(
        label='zone_name',
        source='zone',
        many=True
    )

    name = serializers.CharField(
        label='name'
    )

    host_name = serializers.CharField(
        label='host_name'
    )

    state = serializers.CharField(
        label='state'
    )

    date_offline = serializers.DateTimeField(
        label='date_offline'
    )

    date_first_registered = serializers.DateTimeField(
        label='date_first_registered'
    )

    os_version = serializers.CharField(
        label='os_version'
    )

    ip_address = IPSerializer(
        label='ip_address',
        source='ipaddress_set',
        many=True
    )

    mac_address = MACSerializer(
        label='mac_address',
        source='macaddress_set',
        many=True
    )

    # 실제 정의하는 곳
    class Meta:
        model = Device
        fields = (
            'tenant_name',
            'zone_name',
            'name',
            'host_name',
            'state',
            'date_offline',
            'date_first_registered',
            'os_version',
            'ip_address',
            'mac_address'
    )


class AgentVersionPerTenantSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(
        label='tenant_name'
    )

    rate = serializers.IntegerField(
        label='rate'
    )

    td_total = serializers.IntegerField(
        label='td_total'
    )

    update_count = serializers.IntegerField(
        label='update_count'
    )

    unupdate_count = serializers.IntegerField(
        label='unupdate_count'
    )

    fourty_count = serializers.IntegerField(
        label='fourty_count'
    )

    thirtyfour_count = serializers.IntegerField(
        label='thirtyfour_count'
    )

    thirty_count = serializers.IntegerField(
        label='thirty_count'
    )

    twenty_count = serializers.IntegerField(
        label='twenty_count'
    )

    # 실제 정의하는 곳
    class Meta:
        model = Tenant
        fields = (
            'tenant_name',
            'rate',
            'td_total',
            'update_count',
            'unupdate_count',
            'fourty_count',
            'thirtyfour_count',
            'thirty_count',
            'twenty_count'
        )
