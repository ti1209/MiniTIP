import requests

from policy.models import Policy
from tenant.models import Tenant
from zone.models import Zone
from common.datetime import iso_to_datetime


class ZoneSync:
    def __call__(self):
        return self.sync()

    def sync(self, access_token):
        count = Policy.objects.count()
        zone = requests.get('https://protectapi-au.cylance.com/zones/v2?page=1&page_size=100', headers={
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + access_token,
        })

        for row in zone.json()['page_items']:
            tenant = Tenant.objects.first()

            for re in range(count):
                if row['policy_id'] == Policy.objects.all()[re].po_num:
                    policy = Policy.objects.all()[re].id

            Zone.objects.update_or_create(
                tenant_id=tenant.pk,
                zo_num=row["id"],
                name=row["name"],
                criticality=row["criticality"],
                update_type=row["update_type"],
                zone_rule_id=row["zone_rule_id"],
                policy_id=policy,
                date_created=iso_to_datetime(row["date_created"]),
                date_modified=iso_to_datetime(row["date_modified"])
            )

        return True
