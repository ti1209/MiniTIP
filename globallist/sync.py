import requests

from tenant.models import Tenant
from threat.models import Threat
from globalList.models import GlobalList
from common.datetime import iso_to_datetime


class GlobalistSync:

    def __call__(self):
        return self.sync()

    def sync(self, access_token):
        for page in range(2):
            globalist = requests.get('https://protectapi-au.cylance.com/globallists/v2?listTypeId={0}&page=7&page_size=200'.format(page),
                                     headers={
                                         'Accept': 'application/json',
                                         'Authorization': 'Bearer ' + access_token,
                                     })

            for re in range(globalist.json()['total_pages']):
                globalist = requests.get('https://protectapi-au.cylance.com/globallists/v2?listTypeId={1}&page={0}&page_size=200'
                                 .format(re+1, page), headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token,})

                for row in globalist.json()['page_items']:
                    tenant = Tenant.objects.first()

                    if Threat.objects.filter(sha256=row["sha256"]).exists():
                        threat = Threat.objects.get(sha256=row["sha256"])
                    else:
                        threat = None

                    GlobalList.objects.update_or_create(
                        threat=threat,
                        tenant_id=tenant.pk,
                        name=row["name"],
                        sha256=row["sha256"],
                        md5=row["md5"],
                        cylance_score=row["cylance_score"],
                        av_industry=row["av_industry"],
                        classification=row["classification"],
                        sub_classification=row["sub_classification"],
                        list_type=row["list_type"],
                        category=row["category"],
                        added=iso_to_datetime(row["added"]),
                        added_by=row["added_by"],
                        reason=row["reason"]
                    )

        return True
