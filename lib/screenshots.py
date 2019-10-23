#!/usr/bin/env python
# encoding: utf-8

'''
@Author: Vulkey_Chen (admin@gh0st.cn)
@Blog: https://gh0st.cn
@Data: 2019-04-25
@Team: Mystery Security Team (MSTSEC)
@Function: screenshots
'''

import sys
from selenium import webdriver

def screenshots(browser_path,output_path,urls):
    screenshots_path = {}
    for i in urls:
        if 'phantomjs' in browser_path:
            driver = webdriver.PhantomJS(executable_path=browser_path)
        else:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--hide-scrollbars")
            options.add_argument("--mute-audio")
            options.add_argument("--disable-notifications")
            options.add_argument("--no-first-run")
            options.add_argument("--disable-crash-reporter")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--incognito")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-sync")
            options.add_argument("--no-default-browser-check")
            driver = webdriver.Chrome(chrome_options=options,executable_path=browser_path)
        driver.maximize_window()
        try:
            driver.get(i)
        except:
            continue
        s = '/screenshots/' + i.replace(':', '_').replace('//', '_') + '.png'
        spath = output_path.replace('/screenshots/','') + s
        driver.get_screenshot_as_file(spath)
        screenshots_path[i] = '.' + s
        driver.close()
        sys.stdout.write(' - %s: \033[1;32mscreenshot successful\033[0m.\n' % i)
    return screenshots_path