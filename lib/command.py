#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
@Author: Vulkey_Chen (admin@gh0st.cn)
@Blog: https://gh0st.cn
@Data: 2019-04-25
@Team: Mystery Security Team (MSTSEC)
@Function: command
'''

import argparse

def command_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
            help="Input a filename or a domain.",
            required="True", action="store")
    parser.add_argument("-p", "--ports",
            help="Input ports if you want.",
            required="True", action="store")
    parser.add_argument("-t", "--threadnum",
            help="Input thread number.",
            required="True", action="store")
    parser.add_argument("-m", "--model",
            help="Tool's Model: 1.s->scanner 2.r->reporter.",
            required="True", action="store")
    parser.add_argument("-b", "--browser",
            help="Input browser: 1.p->phantomjs 2.c->chrome",
            required="True", action="store")
    args = parser.parse_args()
    return args