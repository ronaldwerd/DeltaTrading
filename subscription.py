"""
Demonstrates streaming feature in OANDA open api

To execute, run the following command:

python streaming.py [options]

To show heartbeat, replace [options] by -b or --displayHeartBeat
"""

import credentials
import requests
import json

from dateutil import parser
from optparse import OptionParser
from finance_objects import Quote

ACCESS_HEADERS = {'Authorization': 'Bearer ' + credentials.ACCESS_TOKEN}


def get_historical(cross, date_time, bar_count):

    pass


def __oanda_json_to_quote(json_str):
    d = json.loads(json_str)['tick']

    q = Quote()
    q.cross = d['instrument']
    q.date_time = parser.parse(d['time'])
    q.bid = d['bid']
    q.ask = d['ask']
    return q


def quote():
    pass


def connect_to_stream():

    """
    Environment                 Description
    fxTrade (Live)              The live (real money) environment
    fxTrade Practice (Demo)     The demo (simulated money) environment
    """

    # Replace the following variables with your personal values
    access_token = '86101226aca6ccaa99f5826b5b2abb8d-41c96a6b0fb2f775e8cb86a2f413a459'
    account_id = '6284575'
    instruments = 'GBP_JPY'

    try:
        s = requests.Session()
        url = "https://" + credentials.DOMAIN + "/v1/prices"

        params = {'instruments': instruments,
                  'accountId': account_id}

        req = requests.Request('GET', url, ACCESS_HEADERS, params=params)
        pre = req.prepare()
        resp = s.send(pre, stream=True, verify=True)
        return resp
    except Exception as e:
        s.close()
        print("Caught exception when connecting to stream\n" + str(e))


def demo(displayHeartbeat):
    response = connect_to_stream()
    if response.status_code != 200:
        print(response.text)
        return
    for line in response.iter_lines(1):
        if line:
            try:
                line = line.decode('utf-8')
                msg = json.loads(line)
            except Exception as e:
                print("Caught exception when converting message into json\n" + str(e))
                return

            if "instrument" in msg or "tick" in msg or displayHeartbeat:
                print(line)
                q = __oanda_json_to_quote(line)
                print(q)


def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-b", "--displayHeartBeat", dest = "verbose", action = "store_true",
                        help = "Display HeartBeat in streaming data")
    displayHeartbeat = False

    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments")
    if options.verbose:
        displayHeartbeat = True
    demo(displayHeartbeat)


if __name__ == "__main__":
    main()

