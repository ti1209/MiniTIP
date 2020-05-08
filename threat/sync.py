import requests

from device.models import Device
from tenant.models import Tenant
from threat.models import Threat, ThreatDevices
from common.datetime import iso_to_datetime


class ThreatSync:

    def __call__(self):
        return self.sync()

    def sync(self, access_token):
        threat = requests.get('https://protectapi-au.cylance.com/threats/v2?page=1&page_size=200', headers={
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + access_token,
        })

        for re in range(threat.json()['total_pages']):
            threat = requests.get('https://protectapi-au.cylance.com/threats/v2?page={0}&page_size=200'.format(re+1), headers={
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + access_token,
        })

            for row in threat.json()['page_items']:
                tenant = Tenant.objects.first()

                Threat.objects.update_or_create(
                    name=row["name"],
                    sha256=row["sha256"],
                    md5=row["md5"],
                    cylance_score=row["cylance_score"],
                    av_industry=row["av_industry"],
                    classification=row["classification"],
                    sub_classification = row["sub_classification"],
                    Global_Quarantined = row["global_quarantined"],
                    safelisted = row["safelisted"],
                    file_size = row["file_size"],
                    unique_to_cylance = row["unique_to_cylance"],
                    last_found=iso_to_datetime(row["last_found"]),
                    tenant_id=tenant.pk
                )

        for device in Device.objects.all():
            threat_device = requests.get(
                'https://protectapi-au.cylance.com/devices/v2/{0}/threats?page=1&page_size=200'.format(device.de_num),
                headers={
                    'Accept': 'application/json',
                    'Authorization': 'Bearer ' + access_token, })

            for i in range(threat_device.json()['total_number_of_items']):
                for row in threat_device.json()['page_items']:
                    if Threat.objects.filter(sha256=row['sha256']).exists():
                        threat = Threat.objects.filter(sha256=row['sha256']).first()

                    ThreatDevices.objects.update_or_create(
                        datetime = iso_to_datetime(row['date_found']),
                        path = row['file_path'],
                        file_status = row['file_status'],
                        device = device,
                        threat = threat
                    )

        return True
