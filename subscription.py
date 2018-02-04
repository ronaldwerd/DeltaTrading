"""
Demonstrates streaming feature in OANDA open api

To execute, run the following command:

python streaming.py [options]

To show heartbeat, replace [options] by -b or --displayHeartBeat
"""

import credentials
import requests
import json
import v20

from dateutil import parser
from finance_objects import Quote

ACCESS_HEADERS = {'Authorization': 'Bearer ' + credentials.ACCESS_TOKEN}
__ACCESS_TOKEN = ""


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


def get_historical(cross, bar_count): # time_frame, date_time_start, date_time_end
    try:
        s = requests.Session()
        url = "https://" + credentials.DOMAIN + "/v3/instruments/" + cross + '/candles'

        params = {
                  'granularity': 'M5',
                  'count': bar_count}

        req = requests.Request('GET', url, ACCESS_HEADERS, params=params)
        pre = req.prepare()
        resp = s.send(pre, stream=True, verify=True)
        return resp
    except Exception as e:
        s.close()
        print("Caught exception when connecting to stream\n" + str(e))
    pass


def connect_to_stream():

    """
    Environment                 Description
    fxTrade (Live)              The live (real money) environment
    fxTrade Practice (Demo)     The demo (simulated money) environment
    """
    instruments = 'GBP_JPY'

    try:
        s = requests.Session()
        url = "https://" + credentials.DOMAIN + "/v1/prices"

        params = {'instruments': instruments,
                  'accountId': credentials.ACCOUNT_ID}

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
    api = v20.Context(
        credentials.HOSTNAME,
        credentials.PORT,
        token=credentials.ACCESS_TOKEN
    )

    r = api.instrument.candles("USD_CAD")

    print("X")


if __name__ == "__main__":
    main()

