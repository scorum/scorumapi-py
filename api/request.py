import requests
import json
import time

from api.methods import get_api_name, to_payload


def get_curl_cli(url, api, method, args):
    payload = to_payload(method, api, args)
    return "curl --data '{payload}' {url}".format(payload=json.dumps(payload), url=url)


def call(url, api, method, args, retries=5):
    payload = to_payload(method, api, args)

    # print(payload)

    while retries:
        try:
            r = requests.post(url, json=payload)
            retries = 0
        except:
            print("error during request")
            time.sleep(0.5)

    try:
        response = json.loads(r.text)
        # return (response["result"], r.status_code)
        return response["result"]
    except:
        print("request failed with code: %d: %s" % (r.status_code, r.reason))
        print(r.text)
        return None
