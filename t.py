import time
import sh
import json
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


def get_stat(start, end, profile, inst_name):
    raw = sh.aws(
            '--profile',
            profile,
            'lightsail',
            'get-instance-metric-data',
            '--instance-name',
            inst_name,
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

    profiles = {
            'tokyo2': [
                'AWS-Tokyo-2',
                ],
            'sydney': [
                'Ubuntu-512MB-Sydney-1'
                ],
            'seoul': [
                'Ubuntu-512MB-Seoul-1',
                ],
            'tokyo1': [
                'Ubuntu-512MB-Tokyo-1',
                ],
            'sgp': [
                'AWS-Singapore-1',
                ],
            }

    today = date.today()
    d = today - relativedelta(months=1)
    clear_day = {
            'Ubuntu-512MB-Sydney-1':
                datetime.datetime(d.year, d.month, 25, 0, 0, 0),
            'Ubuntu-512MB-Seoul-1':
                datetime.datetime(d.year, d.month, 23, 0, 0, 0),
            'Ubuntu-512MB-Tokyo-1':
                datetime.datetime(d.year, d.month, 25, 0, 0, 0),
            'AWS-Singapore-1':
                datetime.datetime(d.year, d.month, 23, 0, 0, 0),
            'AWS-Tokyo-2':
                datetime.datetime(d.year, d.month, 11, 0, 0, 0),
            }

    for profile in profiles:
        for inst in profiles[profile]:
            print(inst)
            print(clear_day[inst])
            '''
            print('Past 24h usage:\t{0:.2f}\tMB'.format(
                get_stat(yesterday, now, profile, inst)))
            print('Past week usage:\t{0:.2f}\tMB'.format(
                get_stat(week_ago, now, profile, inst)))
            '''
            print('Cycle usage:\t{0:.2f}\tMB'.format(
                get_stat(time.mktime(clear_day[inst].timetuple()),
                    now, profile, inst)))


if __name__ == '__main__':
    main()

