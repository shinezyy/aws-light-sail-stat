import time
import sh
import json
import random as rd


ip = ''

def print_ret(s, j):
    r = str(j)
    js = json.loads(r)
    print(s)
    print(js)
    return r


while not (ip.startswith('54.238') or ip.startswith('54.95')):

    raw = sh.aws('lightsail', 'allocate-static-ip', '--profile', 'tokyo2',
            '--static-ip-name', 'try')
    print_ret('Allocation msg:', raw)
    time.sleep(2)

    raw = sh.aws('lightsail', 'attach-static-ip', '--static-ip-name',
            'try', '--profile', 'tokyo2',
            '--instance-name', 'AWS-Tokyo-2')
    print_ret('Attach msg:', raw)
    time.sleep(2)

    raw = sh.aws('lightsail', 'get-instance', '--profile', 'tokyo2',
            '--instance-name', 'AWS-Tokyo-2')
    r = print_ret('Instance message after allocation:', raw)
    ip = json.loads(r)['instance']['publicIpAddress']
    print(ip)
    if ip.startswith('54.238') or ip.startswith('54.95'):
        break
    time.sleep(2)


    raw = sh.aws('lightsail', 'release-static-ip', '--static-ip-name', \
            'try', '--profile', 'tokyo2')
    r = print_ret('Release message:', raw)
    time.sleep(2)

    raw = sh.aws('lightsail', 'get-instance', '--profile', 'tokyo2',
            '--instance-name', 'AWS-Tokyo-2')
    r = print_ret('Instance message after releasing:', raw)
    ip = json.loads(r)['instance']['publicIpAddress']
    print(ip)
    time.sleep(2)


