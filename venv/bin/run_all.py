#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import time

os.system("python3 /opt/itump/easyump/itmapp/bin/import_app_info.py 1>/opt/itump/easyump/itmapp/logs/run_all.log 2>&1")
time.sleep(5)

os.system("python3 /opt/itump/easyump/itmapp/bin/import_agent_info.py 1>/opt/itump/easyump/itmapp/logs/run_all.log 2>&1")
time.sleep(5)

os.system("python3 /opt/itump/easyump/itmapp/bin/import_group.py 1>/opt/itump/easyump/itmapp/logs/run_all.log 2>&1")
time.sleep(5)

os.system("python3 /opt/itump/easyump/itmapp/bin/import_iptoapp.py 1>/opt/itump/easyump/itmapp/logs/run_all.log 2>&1")
time.sleep(5)

os.system("python3 /opt/itump/easyump/itmapp/bin/import_sit_info.py 1>/opt/itump/easyump/itmapp/logs/run_all.log 2>&1")
time.sleep(5)

os.system("python3 /opt/itump/easyump/itmapp/bin/import_sit_enrich.py 1>/opt/itump/easyump/itmapp/logs/run_all.log 2>&1")
time.sleep(5)

os.system("python3 /opt/itump/easyump/itmapp/bin/process_agent_enrich.py 1>/opt/itump/easyump/itmapp/logs/run_all.log 2>&1")
time.sleep(5)

os.system("python3 /opt/itump/easyump/itmapp/bin/process_itm_policy.py 1>/opt/itump/easyump/itmapp/logs/run_all.log 2>&1")
time.sleep(5)

os.system("python3 /opt/itump/easyump/itmapp/bin/process_ump_policy.py 1>/opt/itump/easyump/itmapp/logs/run_all.log 2>&1")
