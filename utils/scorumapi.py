import api

import sys
import argparse
import logging
import json

pygments_installed = True

try:
    from pygments import highlight, lexers, formatters
except:
    pygments_installed = False


def setup_logger(verbose=False):
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)

    if (verbose):
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

#    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#    ch.setFormatter(formatter)

    root.addHandler(ch)


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-v", dest='verbose', default=False, action='store_true', help='')
    parser.add_argument("-s", dest='secure', default=False, action='store_true', help='')
    parser.add_argument('--host', dest='host', action='store', default='', help='')
    parser.add_argument('--api', dest='api', action='store', default='', help='')
    parser.add_argument('--method', dest='method', action='store', default='', help='')
    parser.add_argument('--args', dest='args', nargs='*', action='store', default=[], help='')

    parser.add_argument('--no-color', dest='nocolors', action='store', default=False, help='')

    opt = parser.parse_args()

    setup_logger(opt.verbose)

    if opt.api is "" and opt.method is "":
        opt.api = "database_api"
        opt.method = "get_dynamic_global_properties"

    if opt.host is "":
        opt.host = "prodnet.scorum.com"
        opt.secure = True

    if opt.secure:
        protocol = "https://"
    else:
        protocol = "http://"

    url = protocol + opt.host + "/rpc"

    logging.debug(url)

    logging.debug(api.get_curl_cli(url, opt.api, opt.method, opt.args))

    response = api.call(url, opt.api, opt.method, opt.args)

    if response is not None:
        formatted_json = json.dumps(response, indent=4, sort_keys=True)

        if not opt.nocolors and pygments_installed:
            formatted_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())

        logging.info(formatted_json)