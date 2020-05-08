import requests

from device.models import Device
from policy.models import Policy
from tenant.models import Tenant
from zone.models import Zone
from common.datetime import iso_to_datetime


class DeviceSync:

    def __call__(self):
        return self.sync()

    def sync(self, access_token):
        device = requests.get('https://protectapi-au.cylance.com/devices/v2?page=1&page_size=100', headers={
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + access_token,
        })

        for row in device.json()['page_items']:
            tenant = Tenant.objects.first()

            if Policy.objects.filter(po_num=row['policy']['id']).exists():
                policy = Policy.objects.filter(po_num=row['policy']['id']).first()

            Device.objects.update_or_create(
                policy=policy,
                tenant_id=tenant.pk,
                de_num=row['id'],
                name=row["name"],
                state=row["state"],
                agent_version = row["agent_version"],
                date_first_registered = iso_to_datetime(row["date_first_registered"]),
                ip_addresses = row["ip_addresses"],
                mac_addresses = row["mac_addresses"]
            )

        for zone in Zone.objects.all():
            device_zone = requests.get(
                'https://protectapi-au.cylance.com/devices/v2/{0}/devices?page=1&page_size=200'.format(zone.zo_num),
                headers={
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + access_token,
                })

            for i in range(device_zone.json()['total_number_of_items']):
                for row in device_zone.json()['page_items']:
                    if Device.objects.filter(de_num=row['id']).exists():
                        device = Device.objects.filter(de_num=row['id']).first()
                        zone.device.add(device)

        return True
