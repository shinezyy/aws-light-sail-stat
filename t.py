import time
import sh
import json


def get_stat(start, end):
    raw = sh.aws('lightsail',
            'get-instance-metric-data',
            '--instance-name',
            'Ubuntu-512MB-Tokyo-1',
            '--metric-name',
            'NetworkOut',
            '--period',
            '2700000',
            '--start-time',
            str(start),
            '--unit',
            'Bytes',
            '--statistics',
            'Sum',
            '--end-time',
            str(end),
            )
    js = json.loads(str(raw))
    return js['metricData'][0]['sum'] / 2**20


def main():
    now = round(time.time())
    a_day = 60*60*24
    yesterday = now - a_day
    week_ago = now - a_day*7
    month_ago = now - a_day*30

    print('The past 24h usage:\t{0:.2f}\tMB'.format(get_stat(yesterday, now)))
    print('The past week usage:\t{0:.2f}\tMB'.format(get_stat(week_ago, now)))
    print('The path month usage:\t{0:.2f}\tMB'.format(get_stat(month_ago, now)))


if __name__ == '__main__':
    main()

