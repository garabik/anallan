#!/usr/bin/python3

import sys, re, subprocess, time
from random import random, randint, choice


from pprint import pprint

import threading
from queue import Queue

machines = {} # mac: {ipv4:xxx, ipv6:xxx}

def get_ipv6_addrs():
    output = subprocess.getoutput('ip -6 neigh show')
    r = {}
    for line in output.splitlines():
        l = line.strip()
        if l.endswith('FAILED') or l.endswith('INCOMPLETE'):
            continue
        ip6, dummy, iface, dummy, mac, rest = l.split(None, 5)
        if mac in r and ip6.startswith('fe80'): # do not overwrite good ipv6 with link-local
            continue
        r[mac] = ip6
    return r

def get_ipv4_addrs():
    output = subprocess.getoutput('ip -4 neigh show')
    r = {}
    for line in output.splitlines():
        l = line.strip()
        if l.endswith('FAILED') or l.endswith('INCOMPLETE'):
            continue
        ip, dummy, iface, dummy, mac, rest = l.split(None, 5)
        status = rest
        r[mac] = (ip, status)
    return r

def nmblookup(ip):
    status, output = subprocess.getstatusoutput('nmblookup -A '+str(ip))
    if status != 0: # error
        return
    lines = output.splitlines()
    lines = [x.strip() for x in lines]
    name = lines[0].split()[0].strip()
    macaddr = None
    for l in lines:
        if 'MAC Address =' in l:
            macaddr = l.split('=')[1].strip().lower().replace('-', ':')
    return name, macaddr

def nmbscan(ip):
    status, output = subprocess.getstatusoutput('/usr/sbin/nmbscan -h '+str(ip))
    if status != 0:
        return
    lines = output.splitlines()
    lines = [x.strip() for x in lines]
    data = {}
    for l in lines:
        if ' ' in l:
            k, v = l.split(' ', 1)
            k = k.strip(); v = v.strip()
            data[k] = v
    domain = data.get('domain', '')
    name = data.get('server', '')
    macaddr = data.get('arp-mac-address', '').lower()
    os = data.get('operating-system', '')
    return name, macaddr, domain, os

def pinger(ip):
    time.sleep(random())
    print('  {:<15} {}'.format(ip, choice('/\-|')), file=sys.stderr, end='\r'); sys.stderr.flush()
    # discard the output
    time.sleep(2)
    #subprocess.getoutput('ping -c 2 -n '+str(ip))
    print(' ',ip, file=sys.stderr, end='    \r'); sys.stderr.flush()


def nmbinfo(ip, nmbmachines):
    time.sleep(4*random())
    print('  {:<15} {}'.format(ip, choice('/\-|')), file=sys.stderr, end='\r'); sys.stderr.flush()
    name, macaddr, domain, os = nmbscan(ip)
    if macaddr:
        nmbmachines[macaddr] = ip, name, domain, os
    print(' ',ip, file=sys.stderr, end='    \r'); sys.stderr.flush()

def lan4_map(prefix, live_addrs):
    # return ASCII map of online computers
    # live_addrs is a list of living computers
    print ('Map of alive IPv4 computers')
    print(' ', end=' ')
    for col in range(16):
        print('.{:x}'.format(col), end = '')
    print()
    for row in range(16):
        print('{:x}'.format(row), end = '. ')
        for col in range(16):
            byte = row*16+col
            ip = prefix+'.'+str(byte)
            if ip in live_addrs:
                print('x', end = ' ')
            else:
                print(' ', end = ' ')
        print()


def ipv6pinger():
    # wake up ipv6 link local machines
    subprocess.getstatusoutput('ping6 -c 2 -I eth0 ff02::1')
    subprocess.getstatusoutput('ping6 -c 2 -B -I eth0 -I 2002:3e98:e80a:1::1 ff02::1')

def worker(q, work):
    while True:
        item = q.get()
        work(item)
        q.task_done()

print('pinging the LAN...')
# wake up machines by pinging all of them
thread_list = []

q = Queue()

for i in range(40):
    t= threading.Thread(target=worker, args=(q,pinger))
    t.daemon = True
    t.start()


for i in range(1, 254):
    ip = '192.168.10.'+str(i)
    q.put(ip)

q.join()
print('he')
time.sleep(10)

