#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pradeep Jairamani , github.com/pradeepjairamani

import socket
import socks
import time
import json
import threading
import string
import random
import sys
import struct
import re
import os
from OpenSSL import crypto
import ssl
from core.alert import *
from core.targets import target_type
from core.targets import target_to_host
from core.load_modules import load_file_path
from lib.socks_resolver.engine import getaddrinfo
from core._time import now
from core.log import __log_into_file
from core.decor import socks_proxy, main_function


def extra_requirements_dict():
    return {
        "Proftpd_vuln_ports": [21, 990]
    }



def cpu_consumption(target, port, timeout_sec, log_in_file, language, time_sleep,
                    thread_tmp_filename, socks_proxy, scan_id, scan_cmd):
    try:
        

        from core.conn import connection
        s = connection(target, port, timeout_sec, socks_proxy)
        if not s:
            return False
        else:
            s.send("ehlo")
            banner = s.recv(100)
            banner = banner.split(" ")
            if banner[1] == "Proftpd":
                vuln_list = ["1.2.0", "1.2.0pre9", "1.2.0pre10", "1.2.0rc1", "1.2.0rc2", "1.2.0rc3", "1.2.1", "1.2.2", "1.2.2rc1", "1.2.2rc2", "1.2.2rc3", "1.2.3", "1.2.4", "1.2.5", "1.2.5rc1", "1.2.5rc2", "1.2.5rc3", "1.2.6rc1", "1.2.6rc2", "1.2.6", "1.2.7rc2", "1.2.7rc3", "1.2.7", "1.2.7rc1",
                             "1.2.8rc2", "1.2.8", "1.2.8rc1", "1.2.9", "1.2.9rc1", "1.2.9rc2", "1.2.9rc3", "1.2.10rc1", "1.2.10rc2", "1.2.10rc3", "1.2.10", "1.3.0a", "1.3.0rc2", "1.3.0rc3", "1.3.0rc4", "1.3.0rc5", "1.3.0", "1.3.0rc1", "1.3.1rc1", "1.3.1rc2", "1.3.1rc3", "1.3.1", "1.3.2", "1.3.2rc2", "1.3.2rc1"]
                if banner[2] in vuln_list:
                    return True
                else:
                    return False
            else:
                return False
    except Exception as e:
        # some error warning
        return False


def __cpu_consumption(target, port, timeout_sec, log_in_file, language, time_sleep,
                      thread_tmp_filename, socks_proxy, scan_id, scan_cmd):
    if cpu_consumption(target, port, timeout_sec, log_in_file, language, time_sleep,
                       thread_tmp_filename, socks_proxy, scan_id, scan_cmd):
        info(messages(language, "target_vulnerable").format(target, port,
                                                            'The pr_data_xfer function in ProFTPD before 1.3.2rc3 allows remote authenticated users to cause a denial of service (CPU consumption) via an ABOR command during a data transfer.	CVE-2008-7265'))
        __log_into_file(thread_tmp_filename, 'w', '0', language)
        data = json.dumps({'HOST': target, 'USERNAME': '', 'PASSWORD': '', 'PORT': port, 'TYPE': 'Proftpd_cpu_consumption_vuln',
                           'DESCRIPTION': messages(language, "vulnerable").format('The pr_data_xfer function in ProFTPD before 1.3.2rc3 allows remote authenticated users to cause a denial of service (CPU consumption) via an ABOR command during a data transfer.	CVE-2008-7265'), 'TIME': now(),
                           'CATEGORY': "vuln",
                           'SCAN_ID': scan_id, 'SCAN_CMD': scan_cmd})
        __log_into_file(log_in_file, 'a', data, language)
        return True
    else:
        return False

@main_function(extra_requirements_dict(), __cpu_consumption, "Proftpd_cpu_consumption_vuln", "ProFTPd CPU consumption	CVE-2008-7265")
def start(target, users, passwds, ports, timeout_sec, thread_number, num, total, log_in_file, time_sleep, language,
          verbose_level, socks_proxy, retries, methods_args, scan_id, scan_cmd):  # Main function
    pass