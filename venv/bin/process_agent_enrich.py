#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import csv
from sub_common import *

# 特定参数
conf = get_conf()
SOURCE_FIE = conf.get("SOURCE_FILE", "AGENT_ENRICH_CONF")
TABLE_NAME = "ITM_AGENT_ENRICH"

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
    process_agent_enrich()

    logger.info("Success insert records:%s.",counter)

def import_agent_enrich():
    global  counter
    counter = 0
    conn = get_conn()
    cursor = conn.cursor()
    with open(SOURCE_FIE,encoding="UTF-8") as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            sql = "insert into {0} (WRITE_TIME,AGENT_TYPE,MO_TYPE,KEYWORD) values(%s,%s,%s,%s)".format(TABLE_NAME)
            cursor.execute(sql,(write_time,row['AGENT_TYPE'],row['MO_TYPE'],row['KEYWORD']))
            counter += 1
    conn.commit()
    conn.close()

def process_agent_enrich():
    conn = get_conn()
    cursor = conn.cursor()
    sql = "select AGENT_TYPE,MO_TYPE,KEYWORD from {0}".format(TABLE_NAME)
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        agent_type = row[0]
        mo_type = row[1]
        keyword = row[2]
        sqlStr = "update ITM_AGENT_INFO set MO_TYPE={0},KEYWORD={1} where AGENT_TYPE = {2}".format(mo_type,keyword,agent_type)
        logger.info("Run sql:%s.",sqlStr)
        cursor.execute(sqlStr)
    conn.commit()
    conn.close()


if __name__ == '__main__':
        main()