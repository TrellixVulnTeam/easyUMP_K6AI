#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import datetime
import sys
import logging
import pymysql
import os
import configparser

#文件示例： NT_TCP_STATUS_HT&&Primary:BL685762:NT Primary:BL685765:NT Primary:HP-BL685-019:NT Primary:HP-BL685-054:NT


# read config
cur_path=os.path.dirname(os.path.realpath(__file__))
config_path=os.path.join(cur_path,'../conf/config.ini')
conf = configparser.ConfigParser()
conf.read(config_path,encoding='utf-8-sig')
DB_IP = conf.get("MYSQL", "DB_IP")
DB_PORT = conf.get("MYSQL", "DB_PORT")
DB_USER = conf.get("MYSQL", "DB_USER")
DB_PASSWORD = conf.get("MYSQL", "DB_PASSWORD")
DB_SCHEMA = conf.get("MYSQL", "DB_SCHEMA")
DB_CHARSET = conf.get("MYSQL", "DB_CHARSET")


# 特定参数
SOURCE_FILE = conf.get("SOURCE_FILE", "GROUP_INFO")
LOG_FILE = conf.get("BASE_CONF", "LOG_PATH") + "/import_group.log"
TABLE_NAME = "itm_group_info"


# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter
counter = 0

# 设置log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE,encoding="UTF-8")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



def main():
    logger.info("Begin to import %s file.",SOURCE_FILE)
    clean_db()
    process_group()
    logger.info("Import %s records.", counter)

def clean_db():
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    sql = "delete from " + TABLE_NAME
    cursor.execute(sql);
    conn.commit();
    print("Table %s has been cleaned!" % TABLE_NAME);
    logger.info("Table %s has been cleaned!",TABLE_NAME)

def import_data(cursor,groupname,agentname):
    global counter
    sqlStr = "insert into {0} (WRITE_TIME,GROUP_NAME,AGENT_NAME) values (%s,%s,%s)".format(TABLE_NAME)
    cursor.execute(sqlStr, (write_time,groupname,agentname));
    counter += 1

def process_group():
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    with open(SOURCE_FILE, 'r',encoding='UTF-8') as file_to_read:
        for lines in file_to_read.readlines():
            lines_tmp =  lines.split('&&')
            groupname = lines_tmp[0]
            agent_all = lines_tmp[1].split()

            i = 0
            hostname = []
            while i <  len(agent_all):
                import_data(cursor,groupname, agent_all[i])
                i = i + 1
    conn.commit();
    conn.close();


if __name__ == '__main__':
        main()

