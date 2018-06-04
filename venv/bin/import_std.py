#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import csv
from sub_common import *

# 特定参数
conf = get_conf()
SOURCE_FIE = conf.get("SOURCE_FILE", "STD_CONF")
TABLE_NAME = "UMP_STD_CONF"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter

# 设置log
logger = get_logger("import.log")

def main():
    logger.info("Begin to insert to table:%s",TABLE_NAME)

    delsql = "delete from {0} ".format(TABLE_NAME)
    clean_db(delsql)
    logger.info("Table %s has been cleaned!",TABLE_NAME)

    import_agent_enrich()

    logger.info("Success insert records:%s.",counter)

def import_agent_enrich():
    global  counter
    counter = 0
    conn = get_conn()
    cursor = conn.cursor()
    with open(SOURCE_FIE,encoding="UTF-8") as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            sql = "insert into {0} (WRITE_TIME,STD_NAME,FILTER,POLICY_NAME) values(%s,%s,%s,%s)".format(TABLE_NAME)
            cursor.execute(sql,(write_time,row['STD_NAME'],row['FILTER'],row['POLICY_NAME']))
            counter += 1
    conn.commit()
    conn.close()

if __name__ == '__main__':
        main()