#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Cisco DNA Center Get Auth Token

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Gabriel Zapodeanu TME, ENB"
__email__ = "gzapodea@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import sys
import requests
import json
import urllib3
import time

from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings
from requests.auth import HTTPBasicAuth  # for Basic Auth

from config import DNAC_URL, DNAC_PASS, DNAC_USER

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data: data to pretty print
    :return None
    """
    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def get_epoch_current_time():
    """
    This function will return the epoch time for the current time
    :return: epoch time including msec
    """
    epoch = time.time()*1000
    return int(epoch)


def get_dnac_jwt_token(dnac_auth):
    """
    Create the authorization token required to access DNA C
    Call to Cisco DNA C - /api/system/v1/auth/login
    :param dnac_auth - DNA C Basic Auth string
    :return Cisco DNA C Auth Token
    """

    url = DNAC_URL + '/dna/system/api/v1/auth/token'
    header = {'content-type': 'application/json'}
    response = requests.post(url, auth=dnac_auth, headers=header, verify=False)
    response_json = response.json()
    dnac_jwt_token = response_json['Token']
    return dnac_jwt_token


def get_client_info(mac_address, epoch_time, dnac_jwt_token):
    """
    This function will retrieve the client information for the client with the MAC address {mac_address}
    :param mac_address: client MAC address
    :return: client info
    """
    url = DNAC_URL + '/dna/intent/api/v1/client-detail?timestamp=' + str(epoch_time) + '&macAddress=' + mac_address
    header = {'content-type': 'application/json', 'x-auth-token': dnac_jwt_token}
    client_response = requests.get(url, headers=header, verify=False)
    client_json = client_response.json()
    return client_json

def main(client_mac_address):
    """
    This sample script will retrieve from Cisco DNA Center client details information for the client with the
    MAC address {client_mac_address}, at the time the script is executed.
    :param client_mac_address: the client MAC address
    :return: None
    """

    # obtain the Cisco DNA C Auth Token
    dnac_token = get_dnac_jwt_token(DNAC_AUTH)

    # convert present time to epoch time
    current_epoch_time = get_epoch_current_time()

    # check if client is present in the Cisco DNA Center inventory
    client_info = get_client_info(client_mac_address, current_epoch_time, dnac_token)
    print('\nThis is the output of the Client Detail API call')
    pprint(client_info)

    client_ipv4_address = client_info['detail']['hostIpV4']
    client_access_switch = client_info['detail']['clientConnection']
    client_switch_interface = client_info['detail']['port']
    client_access_vlan = client_info['detail']['vlanId']
    client_switchport_state = client_info['topology']['links'][0]['linkStatus']

    # find the overall client healthscore
    client_health_info = client_info['detail']['healthScore']
    for health in client_health_info:
        if health['healthType'] == 'OVERALL':
            client_health_score = health['score']
            break
        else:
            client_health_score = 'UNKNOWN'

    # print all the information
    print('\n\nInformation for the client:')
    print('{0:30s}{1:30s}'.format('MAC Address: ', client_mac_address))
    print('{0:30s}{1:30s}'.format('IPv4 Address: ', client_ipv4_address))
    print('{0:30s}{1:30s}'.format('Access Switch: ', client_access_switch))
    print('{0:30s}{1:30s}'.format('Switchport: ', client_switch_interface))
    print('{0:30s}{1:30s}'.format('Access VLAN: ', str(client_access_vlan)))
    print('{0:30s}{1:30s}'.format('Switchport State:', client_switchport_state))
    print('{0:30s}{1:30s}'.format('Client Overall Healthscore: ', str(client_health_score)))

    print('\n\nEnd of Application "get_wired_client_info.py" Run')

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
