#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
@Author: Vulkey_Chen (admin@gh0st.cn)
@Blog: https://gh0st.cn
@Data: 2019-04-25
@Team: Mystery Security Team (MSTSEC)
@Function: main
'''

import threading,os,time,queue,shutil,sys,platform
from lib import command,portsscan,screenshots,template,urls
from lib.domains import domain_scan

start_time = time.time()
output_path = './subdscan/'
report_html = ""
t_domain = ""
target_path = ""
urls_path = ""
screenshots_path = ""
internal_hosts_path = ""
mutex = threading.Lock()
browser_path = ""
phantomjsPath = sys.path[0] + '/exts/phantomjs/'
chromePath = sys.path[0] + '/exts/chrome/'
start_time = time.time()

def visitDir(path):
    fileNum = 0
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        if os.path.isfile(sub_path):
            fileNum = fileNum + 1
    return fileNum

def main(domain,ports):
    # p->ports, u,u1->urls, h->headers, s->screenshots_path_list, d->domain
    global report_html
    while not domain.empty():
        try:
            mutex.acquire()
            d = domain.get()
            mutex.release()
            body_html = ""
            i, p = portsscan.scan_ports(internal_hosts_path,d,ports)
            if i == '1':
                u = urls.gen_urls(d,p)
                u1,h = urls.url_filter(urls_path,u)
                time.sleep(1.5)
                s = screenshots.screenshots(browser_path,screenshots_path,u1)
                for i in s.keys():
                    #print(i
                    headers_html = ""
                    for e in h[i].keys():
                        #print(e
                        if e != "status_code":
                            headers_html += template.header_html_template % (e,h[i][e])
                    status_code = h[i]['status_code']
                    screenshot_path = s[i]
                    body_html += template.table_html_template % (i,status_code,screenshot_path,screenshot_path,i,headers_html)
                if body_html:
                    report_html += template.body_html_template % body_html
        except Exception as e:
            print(e)
        finally:
            domain.task_done()

if __name__ == '__main__':
    # c -> command
    c = command.command_parser()
    if c:
        domains = c.input
        ports = c.ports
        thread_count_num = c.threadnum
        print('\033[1mInfo:\033[0m \n - SubDReporter is going...')
        # 创建subdscan目录
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # os
        sys_info = platform.system()
        sys_bit = platform.architecture()[0]
        # os -> phantomjs_path
        if sys_info == "Darwin":
            if c.browser == "p":
                browser_path = phantomjsPath + 'phantomjs_for_mac'
            else:
                browser_path = chromePath + 'chromedriver_for_mac'
        elif sys_info == "Windows":
            if c.browser == "p":
                browser_path = phantomjsPath + 'phantomjs.exe'
            else:
                browser_path = chromePath + 'chromedriver.exe'
        elif sys_info == "Linux":
            if c.browser == "p":
                if sys_bit == "32bit":
                    browser_path = phantomjsPath + 'phantomjs_for_linux32'
                elif sys_bit == "64bit":
                    browser_path = phantomjsPath + 'phantomjs_for_linux64'
            else:
                browser_path = chromePath + 'chromedriver_for_linux'
        print(' - System : %s x%s' % (sys_info,sys_bit))
        print(' - Browser Path : %s' % browser_path)
        # model
        if c.model == 'r':
            # model: reporter
            print(' - Model: Subdomains Reporter')
            f = open(domains,'r')
            fcontent = f.readlines()
            total_num = str(len(fcontent))
            # 取文本第一行，并且取其顶级域名
            t_domain = urls.getDomain(fcontent[0]).replace('\n','')
            target_path = output_path + t_domain
        elif c.model == 's':
            # model: scanner
            print(' - Model : Subdomains Scanner')
            t_domain = domains
            target_path = output_path + t_domain
            domains_file = target_path + '/' + domains + '_subdomains.txt'
            fcontent = domain_scan(domains)
            total_num = str(len(fcontent))
        else:
            print(" - Error : Unaviliable Model.")
            sys.exit()
        screenshots_path = target_path + '/screenshots/'
        #print(screenshots_path)
        urls_path = target_path + '/urls.txt'
        internal_hosts_path = target_path + '/internal_host.txt'
        # 创建域名目录
        if not os.path.exists(target_path):
            # 不存在就创建
            os.makedirs(target_path)
            os.makedirs(screenshots_path)
        else:
            # 存在就删掉然后创建
            shutil.rmtree(target_path)
            os.makedirs(target_path)
            os.makedirs(screenshots_path)
        if c.model == 's':
            f = open(domains_file,'w')
            for i in fcontent:
                f.write(i + '\n')
            print(' - Saved in : %s' % domains_file)
        threads = []
        queue = queue.Queue()

        if '443' in ports:
            ports_num = len(ports.split(',')) - 1
        else:
            ports_num = len(ports.split(','))

        print(' - Target : %s' % t_domain)
        print(' - Threads : %s\n' % thread_count_num)
        
        print('\033[1mScan:\033[0m')
        # 添加队列
        fc = list(set(fcontent))
        total_nums = str(len(fc))
        if total_nums != total_num:
            print(' - Total : %s' % total_nums)
        else:
            print(' - Total : %s' % total_nums)
        for i in fc:
            queue.put(i.replace('\n',''))
        f.close()
        # 添加线程
        for i in range(int(thread_count_num)):
            t = threading.Thread(target=main,args=[queue,ports])
            threads.append(t)
        for i in threads:
            i.start()
        queue.join()
        for i in threads:
            i.join()

        m,s = divmod((time.time() - start_time), 60)
        end_time = "%sm%ss" % (str(int(m)),str(int(s)))
        # 生成报告
        res = template.main_html_template % (t_domain,t_domain,report_html,template.footer_html_template)
        res_file = target_path + '/report_' + t_domain + '.html'
        report_file = open(res_file,'w')
        report_file.write(res)
        report_file.close()

        # 获取URL个数
        f = open(urls_path,'r')
        urls_num = len(f.readlines())
        f.close()

        if os.path.exists(internal_hosts_path):
            f = open(internal_hosts_path,'r')
            internal_hosts_num = len(f.readlines())
            f.close()
        else:
            internal_hosts_num = 0

        screenshots_num = visitDir(screenshots_path)
        all_urls_num = ports_num * 2 * urls_num

        #print(all_urls_num)

        # 结束输出
        print('\r\n\r\n\033[1mTime:\033[0m')
        print(' - Duration : %s\r\n' % end_time)

        print('\033[1mScreenshots:\033[0m')
        print(' - Successful : %s' % str(screenshots_num))
        print(' - Failed : %s\r\n' % str(urls_num - screenshots_num))

        print('\033[1mURLs:\033[0m')
        print(' - Successful : %s' % str(urls_num))
        print(' - Failed : %s\r\n' % str(all_urls_num - urls_num))

        
        print('\033[1mInternal Hosts:\033[0m')
        print(' - Number : %s' % str(internal_hosts_num))
        if internal_hosts_num:
            print(' - File : %s' % internal_hosts_path)

        print('\033[1mWrote HTML report to: %s\033[0m' % res_file)