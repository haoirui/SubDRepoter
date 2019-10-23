#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
@Author: Vulkey_Chen (admin@gh0st.cn)
@Blog: https://gh0st.cn
@Data: 2019-04-25
@Team: Mystery Security Team (MSTSEC)
@Function: scan ports
'''

import socket,sys
from functools import reduce

socket.setdefaulttimeout(2)


# First:192.168.1.13 > c0.a8.01.0d
# Second: c0.a8.01.0d > c0a8010d > 3232235789
def ip_into_int(ip):
    return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))

# is internal ip
def is_internal_ip(ip):
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c

def whatRes(res,domain,port):
    if res == 0:
        sys.stdout.write(" - %s: \033[1;32m%s open\033[0m.\n" % (domain,port))

# scan ports
def scan_ports(output_path,domain,ports):
    try:
        ip = socket.gethostbyname(domain) # domain2ip
    except:
        return None,None
    #print ports.split(',')
    open_ports = []
    if is_internal_ip(ip): # is internal ip
        sys.stdout.write(" - %s \033[1;33mInternal IP: %s\033[0m\n" % (domain,ip))
        f = open(output_path,'a+')
        f.write("%s:%s\n" % (domain,ip))
        f.close()
        return '0',ip
    else:
        try:
            for port in ports.split(','):
                s = socket.socket(2,1)
                if '-' in port:
                    x = port.split('-')
                    for i in range(int(x[0]),int(x[1])):
                        res = s.connect_ex((ip,int(i)))
                        whatRes(res,domain,i)
                        open_ports.append(i)
                else:
                    res = s.connect_ex((ip,int(port)))
                    whatRes(res,domain,port)
                    open_ports.append(port)
                s.close()
            return '1',open_ports
        except:
            pass