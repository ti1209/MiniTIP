# import json
# import os
# import sys
# import uuid
# from datetime import datetime, timedelta
#
# import django
# import jwt
# import requests
#
# from MiniTIP.settings import BASE_DIR
#
# sys.path.append(BASE_DIR)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MiniTIP.settings")
#
# django.setup()
#
# from Zone.models import Zone
# from Policy.models import Policy
# from Device.models import Device
# from GlobalList.models import GlobalList
# from Tenant.models import Tenant
# from Threat.models import Threat
# from common.datetime import iso_to_datetime
#
# timeout = 1800
# now = datetime.utcnow()
# timeout_datetime = now + timedelta(seconds=timeout)
# epoch_time = int((now - datetime(1970, 1, 1)).total_seconds())
# epoch_timeout = int((timeout_datetime - datetime(1970, 1, 1)).total_seconds())
#
# jti_val = str(uuid.uuid4())
# tid_val = "166a3615-4392-42ea-a0cf-c86cfb8e9b9a"
# app_id = "38d207be-f88f-4173-a491-4dfec8e12d2a"
# app_secret = "43645836-6146-4f9c-a8c0-99de785c291e"
# AUTH_URL = "https://protectapi-au.cylance.com/auth/v2/token"
#
# claims = {
#     "exp": epoch_timeout,
#     "iat": epoch_time,
#     "iss": "http://cylance.com",
#     "sub": app_id,
#     "tid": tid_val,
#     "jti": jti_val
# }
#
# encoded = jwt.encode(claims, app_secret, algorithm='HS256')
#
# payload = {"auth_token": encoded.decode('utf-8')}
# headers = {"Content-Type": "application/json; charset=utf-8"}
# resp = requests.post(AUTH_URL, headers=headers, data=json.dumps(payload))
# access_token = json.loads(resp.text)['access_token']
#
# headers = {
#     'Accept': 'application/json',
#     'Authorization': 'Bearer ' + access_token,
# }
#
# # globalist
# # for page in range(2):
# #     globalist = requests.get('https://protectapi-au.cylance.com/globallists/v2?listTypeId={0}&page=7&page_size=200'.format(page),
# #                              headers=headers)
# #
# #     for re in range(globalist.json()['total_pages']):
# #         globalist = requests.get('https://protectapi-au.cylance.com/globallists/v2?listTypeId={1}&page={0}&page_size=200'
# #                                  .format(re+1, page), headers=headers)
# #
# #         for row in globalist.json()['page_items']:
# #             tenant = Tenant.objects.first()
# #
# #             if Threat.objects.filter(sha256=row["sha256"]).exists():
# #                 threat = Threat.objects.get(sha256=row["sha256"])
# #                 threat_id = threat.pk
# #             else:
# #                 threat = None
# #
# #             GlobalList.objects.update_or_create(
# #                 defaults={
# #                     "sha256": row["sha256"],
# #                 },
# #                 threat=threat,
# #                 tenant_id=tenant.pk,
# #                 name=row["name"],
# #                 sha256=row["sha256"],
# #                 md5=row["md5"],
# #                 cylance_score=row["cylance_score"],
# #                 av_industry=row["av_industry"],
# #                 classification=row["classification"],
# #                 sub_classification=row["sub_classification"],
# #                 list_type=row["list_type"],
# #                 category=row["category"],
# #                 added=iso_to_datetime(row["added"]),
# #                 added_by=row["added_by"],
# #                 reason=row["reason"]
# #             )
#
#
#
#
# # device
# # device = requests.get('https://protectapi-au.cylance.com/devices/v2?page=1&page_size=100', headers=headers)
# #
# # for row in device.json()['page_items']:
# #     tenant = Tenant.objects.first()
# #
# #     if Policy.objects.filter(po_num=row['policy']['id']).exists():
# #         policy = Policy.objects.filter(po_num=row['policy']['id']).first()
# #
# #     Device.objects.update_or_create(
# #         defaults={
# #             "de_num": row["id"],
# #         },
# #         policy=policy,
# #         tenant_id=tenant.pk,
# #         de_num=row['id'],
# #         name=row["name"],
# #         state=row["state"],
# #         agent_version = row["agent_version"],
# #         date_first_registered = iso_to_datetime(row["date_first_registered"]),
# #         ip_addresses = row["ip_addresses"],
# #         mac_addresses = row["mac_addresses"]
# #     )
#
#
#
#
#
#
#
# # policy
# # policy = requests.get('https://protectapi-au.cylance.com/policies/v2?page=1&page_size=100', headers=headers)
# # for row in policy.json()['page_items']:
# #     1:1 relations
# #     tenant = Tenant.objects.first()
#
# #     po_num = row["id"]
# #     Policy.objects.update_or_create(
# #         defaults={
# #             "po_num": row["id"],
# #         },
# #
# #         tenant_id=tenant.pk,
# #         po_num=row['id'],
# #         name=row["name"],
# #         device_count=row["device_count"],
# #         zone_count=row["zone_count"],
# #         date_added=iso_to_datetime(row["date_added"]),
# #         date_modified=iso_to_datetime(row["date_modified"]),
# #     )
#
#
#
#
#
# # threat
# # threat = requests.get('https://protectapi-au.cylance.com/threats/v2?page=1&page_size=200', headers=headers)
# #
# # for re in range(threat.json()['total_pages']):
# #     threat = requests.get('https://protectapi-au.cylance.com/threats/v2?page={0}&page_size=200'.format(re+1), headers=headers)
# #
# #     for row in threat.json()['page_items']:
# #         tenant = Tenant.objects.first()
# #
# #         Threat.objects.update_or_create(
# #                 defaults={
# #                     "sha256": row["sha256"],
# #                 },
# #                 name=row["name"],
# #                 sha256=row["sha256"],
# #                 md5=row["md5"],
# #                 cylance_score=row["cylance_score"],
# #                 av_industry=row["av_industry"],
# #                 classification=row["classification"],
# #                 sub_classification = row["sub_classification"],
# #                 Global_Quarantined = row["global_quarantined"],
# #                 safelisted = row["safelisted"],
# #                 file_size = row["file_size"],
# #                 unique_to_cylance = row["unique_to_cylance"],
# #                 last_found=iso_to_datetime(row["last_found"]),
# #                 tenant_id=tenant.pk
# #         )
#
#
#
#
#
# # zone
# # count = Policy.objects.count()
# # zone = requests.get('https://protectapi-au.cylance.com/zones/v2?page=1&page_size=100', headers=headers)
# #
# # for row in zone.json()['page_items']:
# #     tenant = Tenant.objects.first()
# #
# #     for re in range(count):
# #         if row['policy_id'] == Policy.objects.all()[re].po_num:
# #             policy = Policy.objects.all()[re].id
# #
# #     Zone.objects.update_or_create(
# #         defaults={
# #             "zo_num": row["id"],
# #         },
# #
# #         tenant_id=tenant.pk,
# #         zo_num=row["id"],
# #         name=row["name"],
# #         criticality=row["criticality"],
# #         update_type=row["update_type"],
# #         zone_rule_id=row["zone_rule_id"],
# #         policy_id=policy,
# #         date_created=iso_to_datetime(row["date_created"]),
# #         date_modified=iso_to_datetime(row["date_modified"])
# #     )
