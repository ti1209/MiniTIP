import requests

from policy.models import Policy
from tenant.models import Tenant
from common.datetime import iso_to_datetime


class PolicySync:

    def __call__(self):
        return self.sync()

    def sync(self, access_token):
        policy = requests.get('https://protectapi-au.cylance.com/policies/v2?page=1&page_size=100', headers={
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + access_token,
        })

        for row in policy.json()['page_items']:
            tenant = Tenant.objects.first()

            Policy.objects.update_or_create(
                defaults={
                    "po_num": row["id"],
                },

                tenant_id=tenant.pk,
                po_num=row['id'],
                name=row["name"],
                device_count=row["device_count"],
                zone_count=row["zone_count"],
                date_added=iso_to_datetime(row["date_added"]),
                date_modified=iso_to_datetime(row["date_modified"]),
            )

        return True
