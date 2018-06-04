#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import datetime
from sub_common import *

# 设置log
logger = get_logger("report.log")

# 特定参数
TABLE_NAME = "UMP_STD_CONF"
STD_NAME = "WEBLOGIC域监控标准"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter
global std_all



def main():
    logger.info("Begin to insert to table:%s",TABLE_NAME)

    global std_all
    std_all = []
    conn = get_conn()
    cursor = conn.cursor()
    sql = "select POLICY_NAME from {0} where STD_NAME = {1} ".format(TABLE_NAME,STD_NAME)
    cursor.execute(sql)
    rows = cursor.fetchall()
    total = len(rows)
    for row in rows:
        std_all.append(row[0])

    sql = "select APP_NAME,IP_ADDRESS,KEY_WORD,POLICY_NAME from UMP_DOC where MO_TYPE = 'WEBLOGIC_DOMAIN' group by KEY_WORD"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        match_policy = 0
        app_name = row[0]
        ip_address = row[1]
        key_word = row[2]
        policy_name = row[3]
        if policy_name in std_all:
            match_policy += 1


    process_import()

    logger.info("Success insert records:%s.",counter)

def process_import():
    global counter
    counter = 0
    conn = get_conn()
    cursor = conn.cursor();
    sql = '''select 
                po.APP_NAME ,po.IP_ADDRESS,po.SIT_NAME, po.SIT_DESC,po.COMPONENT_TYPE,po.COMPONENT,po.SUB_COMPONENT,
                sit.REEV_TIME,sit.MON_PERIOD,sit.THRESHOLD,sit.PDT,sit.SEVERITY,sit.REPEAT_COUNT,
                agt.AGENT_TYPE,agt.MO_TYPE,agt.KEYWORD
            FROM
                ITM_POLICY po,
                ITM_SIT_INFO sit,
                ITM_AGENT_INFO agt
            where
                sit.FORWARD='Y' 
                and po.SIT_NAME = sit.SITNAME
                and po.AGENT_NAME = agt.AGENT_NAME 
        '''
    cursor.execute(sql);
    rows = cursor.fetchall()


if __name__ == '__main__':
        main()