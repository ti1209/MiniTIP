from django.core.management.base import BaseCommand

import json
import uuid
from datetime import datetime, timedelta

import jwt
import requests

# import os
# import sys
# import django
# from MiniTIP.settings import BASE_DIR
#
# sys.path.append(BASE_DIR)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MiniTIP.settings")
#
# django.setup()

from Policy.sync import PolicySync
from Threat.sync import ThreatSync
from Zone.sync import ZoneSync
from GlobalList.sync import GlobalistSync
from Device.sync import DeviceSync


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        timeout = 1800
        now = datetime.utcnow()
        timeout_datetime = now + timedelta(seconds=timeout)
        epoch_time = int((now - datetime(1970, 1, 1)).total_seconds())
        epoch_timeout = int((timeout_datetime - datetime(1970, 1, 1)).total_seconds())

        jti_val = str(uuid.uuid4())
        tid_val = "166a3615-4392-42ea-a0cf-c86cfb8e9b9a"
        app_id = "38d207be-f88f-4173-a491-4dfec8e12d2a"
        app_secret = "43645836-6146-4f9c-a8c0-99de785c291e"
        AUTH_URL = "https://protectapi-au.cylance.com/auth/v2/token"

        claims = {
            "exp": epoch_timeout,
            "iat": epoch_time,
            "iss": "http://cylance.com",
            "sub": app_id,
            "tid": tid_val,
            "jti": jti_val
        }

        encoded = jwt.encode(claims, app_secret, algorithm='HS256')

        payload = {"auth_token": encoded.decode('utf-8')}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        resp = requests.post(AUTH_URL, headers=headers, data=json.dumps(payload))
        access_token = json.loads(resp.text)['access_token']

        policy = PolicySync().sync(access_token)
        print("policy : {0}".format(policy))

        threat = ThreatSync().sync(access_token)
        print("threat : {0}".format(threat))

        device = DeviceSync().sync(access_token)
        print("device : {0}".format(device))

        zone = ZoneSync().sync(access_token)
        print("zone : {0}".format(zone))

        globalist = GlobalistSync().sync(access_token)
        print("globalist : {0}".format(globalist))

        self.stdout.write(self.style.SUCCESS("Success"))

