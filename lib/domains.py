#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
@Author: Meloner (1214924100@qq.com)
@Data: 2019-04-27
@Team: Mystery Security Team (MSTSEC)
@Function: Subdomains API Scanner
'''

import requests,re,json
from bs4 import BeautifulSoup

def is_valid_domain(value):
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    return True if pattern.match(value) else False

def domain_scan(domain):
    # domains = set()
    # temp_domain = domain
    # root_domain = get_topdomain(domain)
    # for item in list(root_domain):
    alldomin = find_domain(domain)
        # domains = domains | alldomin
    return alldomin

def find_domain(domain):
    res = set()
    s = securitytrails(domain)
    f = findsubdomains(domain)
    b = baidu(domain)
    i = ip138(domain)
    v = virustotal(domain)
    if s:
        res = res | s
    if f:
        res = res | f
    if b:
        res = res | b
    if i:
        res = res | i
    if v:
        res = res | v
    return res

def get_topdomain(domain):
    aizhan_set = set()
    aizhan_set.add(domain)
    url1 = 'https://icp.aizhan.com/%s/' % domain
    try:
        r = requests.get(url1)
        b = BeautifulSoup(r.content,'lxml')
        for i in b.find_all('span',class_='blue'):
            if '<br/>' in str(i):
                res = str(i).replace('\t','').replace('<br/>','\n').replace('<span class="blue">\n','').replace('</span>','').split()
                for i in res:
                    if is_valid_domain(i.strip('www.')):
                        aizhan_set.add(i.strip('www.'))
            else:
                try:
                    aizhan_set.add(i.string.strip().strip('www.'))
                except:
                    return None
            continue
        return aizhan_set
    except:
        return None

# domains api function 

# def crt(domain):
#     crt_set = set()
#     url = 'https://crt.sh/?q=%25.' +domain
#     try:
#         r = requests.get(url).content
#         b = BeautifulSoup(r,'lxml')
#         res = b.find_all('td',class_='',style='')
#         for i in res:
#             if '</a>' not in str(i) and '*.' not in str(i):
#                crt_set.add(i.string)
#         return crt_set()
#     except:
#         return None

def virustotal(domain):
    virustotal_set = set()
    url = 'https://www.virustotal.com/vtapi/v2/domain/report?apikey=&domain=' + domain
    try:
        r = requests.get(url)
        r_dict = json.loads(r.text)
        for i in r_dict['subdomains']:
            virustotal_set.add(i)
        return virustotal_set
    except:
        return None

def ip138(domain):
    ip138_set = set()
    url = 'http://site.ip138.com/%s/domain.htm' % domain
    try :
        r = requests.get(url)
        b = BeautifulSoup(r.content,'lxml')
        res = b.find_all('a',href=re.compile(domain),target='_blank',rel='')
        for i in res:
            ip138_set.add(i.string)
        return ip138_set
    except:
        return None

def baidu(domain):
    baidu_set = set()
    url_r = 'http://ce.baidu.com/index/getRelatedSites?site_address=%s' % domain
    try:
        r = requests.get(url_r).content
        jr = json.loads(r)
        urls = jr['data']
        for url in urls:
            url = url['domain']
            baidu_set.add(url)
        return baidu_set
    except:
       return None

def findsubdomains(domain):
    find_set = set()
    url = 'https://findsubdomains.com/subdomains-of/%s' % domain
    try:
        r = requests.get(url).content
        b = BeautifulSoup(r, 'lxml')
        res = b.find_all(attrs={'class': 'js-domain-name domains', 'class': 'domains js-domain-name'})
        for c in res:
            find_set.add(c.string.strip())
    except:
        return None
    try:
        url = "https://api.spyse.com/v1/subdomains?api_token=&domain=%s" % domain
        r = requests.get(url).content
        url = json.loads(r)
        for url2 in url['records']:
            url3 = url2['domain']
            if url3 not in find_set:
                find_set.add(url3)
        return find_set
    except:
        return None

def securitytrails(domain):
    securitytrails_set = set()
    url = "https://api.securitytrails.com/v1/domain/{0}/subdomains".format(domain)
    try:
        querystring = {"apikey":""}
        response = requests.request("GET", url, params=querystring)
        for i in json.loads(response.text)['subdomains']:
            securitytrails_set.add(i + "." + domain)
        return securitytrails_set
    except:
        return None
