import requests
import json
from my_projects.FIFA.user_agents.config import *


api_url = "https://api.whatismybrowser.com/api/v2/user_agent_parse"

headers = {
    'X-API-KEY': api_key,
}

post_data = {
    # "user_agent":
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
    #     "/63.0.3282.167 Safari/537.36",
    "user_agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
        "/60.0.3112.113 Safari/537.36"
}

result = requests.post(api_url, data=json.dumps(post_data), headers=headers)

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

parse = result_json.get('parse')
version_check = result_json.get('version_check')

if parse.get('is_abusive') is True:
    print('BE CAREFUL - this user agent seems abusive')

if parse.get('simple_software_string'):
    print(parse.get('simple_software_string'))

if version_check:

    if version_check.get('is_checkable') is True:

        if version_check.get('is_up_to_date') is True:
            print(f"{parse.get('software_name')} is up to date")
        else:
            print(f"{parse.get('software_name')} is out of date")

            if version_check.get('latest_version'):
                print(f"The latest version is {'.'.join(version_check.get('latest_version'))}")

            if version_check.get('update_url'):
                print(f"You can update here: {version_check.get('update_url')}")
