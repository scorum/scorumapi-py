import requests
import json


methods = {
    "get_dynamic_global_properties": "database_api",
    "get_account_count": "database_api",
    "lookup_account_names": "database_api",
    "lookup_accounts": "database_api",
    "get_discussions_by_created": "tags_api",
    "get_chain_capital": "chain_api"}


def get_api_name(method):
    try:
        api = methods[method]
        return api
    except:
        return None


def call(url, method, args):
    api = get_api_name(method)

    if api is None:
        return None

    return call(url, method, args)


def is_json(myjson):
    try:
        json_object = json.loads(str(myjson))
    except ValueError:
        return False
    return True


def to_payload(api, method, args):
    data = dict()

    data["id"] = "0"
    data["jsonrpc"] = "2.0"
    data["method"] = "call"

    for i, value in enumerate(args):
        if is_json(value):
             args[i] = json.loads(value)

    data["params"] = [api, method, args]

    return data


def get_curl_cli(url, api, method, args):
    if api is "" or api is None:
        api = get_api_name(method)
        if api is "" or api is None:
            raise Exception('there is no api for method: %s' % method)

    payload = to_payload(api, method, args)
    return "curl --data '{payload}' {url}".format(payload=json.dumps(payload), url=url)


def call(url, api, method, args):
    if api is "" or api is None:
        api = get_api_name(method)
        if api is "" or api is None:
            raise Exception('there is no api for method: %s' % method)

    payload = to_payload(api, method, args)

    print(payload)

    r = requests.post(url, json=payload)

    try:
        response = json.loads(r.text)
        # return (response["result"], r.status_code)
        return response["result"]
    except:
        print("request failed with code: %d: %s" % (r.status_code, r.reason))
        print(r.text)
        return None