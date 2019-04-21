import requests
import json
from my_projects.FIFA.user_agents.config import *


api_url = "https://api.whatismybrowser.com/api/v2/software_version_numbers/all"

headers = {
    'X-API-KEY': api_key,
}

result = requests.get(api_url, headers=headers)

result_json = {}
try:
    result_json = result.json()
except Exception as e:
    print(result.text())
    print("Couldn't decode the response as JSON: ", e)
    exit()

if result.status_code != 200:
    print(f"ERROR: not a 200 result. Instead got: {result.status_code}.")
    print(json.dumps(result_json, indent=2))
    exit()

if result_json.get('result', {}).get('code') != 'success':
    print(f"The API did not return a 'success' response. It said: "
          f"result code: {result_json.get('result', {}).get('code')},"
          f"message_code: {result_json.get('result', {}).get('message_code')},"
          f"message: {result_json.get('result', {}).get('message')}")
    exit()

print(json.dumps(result_json, indent=2))

version_data = result_json.get('version_data')

for software_key in version_data:

    print(f"Version data for {software_key}")
    software_version_data = version_data.get(software_key)

    for stream_code_key in software_version_data:

        print(f"\tStream: {stream_code_key}")
        print(f"\tThe latest version number for {software_key} [{stream_code_key}] is "
              f"{'.'.join(software_version_data.get(stream_code_key).get('latest_version'))}")

        if software_version_data.get(stream_code_key).get('update'):
            print(f"\tUpdate no: {software_version_data.get(stream_code_key).get('update')}")

        if software_version_data.get(stream_code_key).get('update_url'):
            print(f"\tUpdate URL: {software_version_data.get(stream_code_key).get('update_url')}")

        if software_version_data.get(stream_code_key).get('download_url'):
            print(f"\tDownload URL: {software_version_data.get(stream_code_key).get('download_url')}")

    print("---------------------------------")
