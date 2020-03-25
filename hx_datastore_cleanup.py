"""
HyperFlex Datastore Cleanup Script v1
Author: Ugo Emekauwa
Contact: uemekauw@cisco.com, uemekauwa@gmail.com
Summary: The HyperFlex Datastore Cleanup Script for Cisco HyperFlex
         utilizes the HyperFlex API to automatically delete any datastores
         that have met or exceeded a specified retention time limit. The ability to
         exempt any datastores from the retention time limit is provided.
"""

# Import needed modules
import sys
import logging
import requests
import json
import urllib3
from datetime import datetime


######################
# Required Variables #
######################
hx_admin = "admin"
hx_password = "C1sco12345"
hx_connect_ip = "192.168.1.100"
hx_datastore_retention_time_limit_hours = 24
hx_exempted_datastores_list = ()


# Suppress InsecureRequestWarning
urllib3.disable_warnings()

# Obtain HyperFlex API access token
hx_token_request_headers = {"Content-Type": "application/json"}
hx_token_request_url = "https://{}/aaa/v1/auth?grant_type=password".format(hx_connect_ip)
hx_token_post_body = {
    "username": hx_admin,
    "password": hx_password,
    "client_id": "HxGuiClient",
    "client_secret": "Sunnyvale",
    "redirect_uri": "http://localhost:8080/aaa/redirect"
    }

try:
    print("Attempting to obtain the HyperFlex API access token...")
    obtain_hx_api_token = requests.post(hx_token_request_url, headers=hx_token_request_headers, data=json.dumps(hx_token_post_body), verify=False)
    if obtain_hx_api_token.status_code == 201:
        hx_api_token_type = obtain_hx_api_token.json()["token_type"]
        hx_api_access_token = obtain_hx_api_token.json()["access_token"]
        print("The HyperFlex API access token was sucessfully obtained.\n")
    else:
        print("There was an error obtaining the HyperFlex API access token: ")
        print("Status Code: {}".format(str(obtain_hx_api_token.status_code)))
        print("{}\n".format(str(obtain_hx_api_token.json())))
        sys.exit(0)
except Exception as exception_message:
    print("There was an error obtaining the HyperFlex API access token: ")
    print("{}\n".format(str(exception_message)))
    sys.exit(0)
    
# Retrieve configured HyperFlex cluster information
hx_cluster_request_headers = {
    "Accept-Language": "application/json",
    "Authorization": "{}{}".format(str(hx_api_token_type), str(hx_api_access_token))
    }
hx_cluster_request_url = "https://{}/coreapi/v1/clusters".format(hx_connect_ip)

try:
    print("Attempting to obtain the HyperFlex cluster configuration information...")
    get_hx_cluster = requests.get(hx_cluster_request_url, headers=hx_cluster_request_headers, verify=False) 
    if get_hx_cluster.status_code == 200:
        hx_cluster = get_hx_cluster.json()
        hx_cluster_name = hx_cluster[0]["name"]
        hx_cluster_uuid = hx_cluster[0]["uuid"]
        print("The HyperFlex cluster named {} with the UUID {} has been found.\n".format(hx_cluster_name, hx_cluster_uuid))
    else:
        print("There was an error obtaining the HyperFlex cluster configuration information: ")
        print("Status Code: {}".format(str(get_hx_cluster.status_code)))
        print("{}\n".format(str(get_hx_cluster.json())))
except Exception as exception_message:
    print("There was an error obtaining the HyperFlex cluster configuration information: ")
    print("{}\n".format(str(exception_message)))

# Retrieve current HyperFlex datastores list
get_hx_datastores_request_headers = {
    "Accept-Language": "application/json",
    "Authorization": "{}{}".format(str(hx_api_token_type), str(hx_api_access_token))
    }
get_hx_datastores_request_url = "https://{}/coreapi/v1/clusters/{}/datastores".format(hx_connect_ip, hx_cluster_uuid)

try:
    print("Attempting to obtain the list of configured HyperFlex datastores...")
    get_hx_datastores = requests.get(get_hx_datastores_request_url, headers=get_hx_datastores_request_headers, verify=False) 
    if get_hx_datastores.status_code == 200:
        hx_datastores = get_hx_datastores.json()
        if not hx_datastores:
            print("No HyperFlex datastores were found.")
            print("\nThe HyperFlex Datastore Cleanup Script is complete.")
            sys.exit(0)
        else:
            print("The following HyperFlex datastores have been found:")
            for index, hx_datastore in enumerate(hx_datastores, start=1):
                if hx_datastore["dsconfig"]["provisionedCapacity"] >= 1099511627776:
                    hx_datastore_size = hx_datastore["dsconfig"]["provisionedCapacity"] / 1099511627776
                    hx_datastore_size_unit = "TB"
                else:
                    hx_datastore_size = hx_datastore["dsconfig"]["provisionedCapacity"] / 1073741824
                    hx_datastore_size_unit = "GB"
                hx_datastore_creation_time = datetime.fromtimestamp(int(hx_datastore["creationTime"])).strftime("%I:%M:%S %p on %A, %B %d, %Y")
                hx_datastore_current_age = str(round((int(datetime.utcnow().timestamp()) - int(hx_datastore["creationTime"])) / 3600, 1))
                print("    {}. {} with a provisioned size of {} {} and a creation time of {}. The approximate age is {} hour(s).".format(index, hx_datastore["dsconfig"]["name"], hx_datastore_size, hx_datastore_size_unit, hx_datastore_creation_time, hx_datastore_current_age))
            print("\n")
    else:
        print("There was an error obtaining the list of configured HyperFlex datastores: ")
        print("Status Code: {}".format(str(get_hx_datastores.status_code)))
        print("{}\n".format(str(get_hx_datastores.json())))
        sys.exit(0)
except Exception as exception_message:
    print("There was an error obtaining the list of configured HyperFlex datastores: ")
    print("{}\n".format(str(exception_message)))
    sys.exit(0)

# Cleanup HyperFlex datastores
delete_hx_datastores_request_headers = {
    "Accept-Language": "application/json",
    "Authorization": "{}{}".format(str(hx_api_token_type), str(hx_api_access_token)),
    }

hx_datastore_retention_time_limit_seconds = hx_datastore_retention_time_limit_hours * 3600

try:
    print("Beginning the cleanup of any HyperFlex datastores that have met or exceeded the set retention time limit of {} hour(s)...\n".format(hx_datastore_retention_time_limit_hours))
    for hx_datastore in hx_datastores:
        if hx_datastore["dsconfig"]["name"] not in hx_exempted_datastores_list:
            if int(datetime.utcnow().timestamp()) >= int(hx_datastore["creationTime"]) + hx_datastore_retention_time_limit_seconds:
                print("The retention time limit for the datastore named {} has been met or exceeded.".format(hx_datastore["dsconfig"]["name"]))
                print("Attempting to delete...")
                delete_hx_datastores_request_url = "https://{}/coreapi/v1/clusters/{}/datastores/{}".format(hx_connect_ip, hx_cluster_uuid, hx_datastore["uuid"])
                delete_hx_datastore = requests.delete(delete_hx_datastores_request_url, headers=delete_hx_datastores_request_headers, verify=False)
                if delete_hx_datastore.status_code == 200:
                    print("The datastore named {} has been deleted.".format(hx_datastore["dsconfig"]["name"]))
                else:
                    print("There was an error deleting the datastore named {}.".format(hx_datastore["dsconfig"]["name"]))
                    print("Status Code: {}\n".format(str(new_hx_datastore.status_code)))
            else:
                print("The datastore named {} has a retention time limit that has not been met or exceeded. No action is needed at this time.".format(hx_datastore["dsconfig"]["name"]))
        else:
            print("The datastore named {} is exempt from any retention time limit. No action will be taken.".format(hx_datastore["dsconfig"]["name"]))
except Exception as exception_message:
    print("There was an error cleaning up the HyperFlex datastores: ")
    print("{}\n".format(str(exception_message)))

# Exiting the HyperFlex Datastore Cleanup Script
print("\nThe HyperFlex Datastore Cleanup Script is complete.")
sys.exit(0)
