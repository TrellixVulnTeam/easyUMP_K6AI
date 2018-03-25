#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import datetime
import sys
import logging
import pymysql
import os
import configparser




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
SOURCE_FILE = conf.get("SOURCE_FILE", "IPTOAPP_FILE")
LOG_FILE = conf.get("BASE_CONF", "LOG_PATH") + "/import_iptoapp.log"
TABLE_NAME = "itm_iptoapp"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter_dup
global counter_err
global counter
counter_dup = 0
counter_err = 0
counter = 0

# 设置log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main():
    global counter_err
    global counter

    clean_db();

    logger.info('开始导入ip to app 数据！')
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    with open(SOURCE_FILE, 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip("\n")
            record = line.split();
            if len(record) == 3:
                ipaddress = record[0];
                app_name = record[1];
                app_code = record[2];
                import_data(cursor,ipaddress,app_name,app_code);
                counter += 1
            else:
                print('格式存在问题的记录:'+ line)
                logger.error('格式存在问题的记录: %s',line)
                counter_err += 1
             #   print("hello")
    conn.commit()
    conn.close()
    logger.info('正常导入%s条记录完成。另，%s条记录重复，%s条格式异常。',counter,counter_dup,counter_err)

def clean_db():
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    sql = "delete from " + TABLE_NAME
    cursor.execute(sql);
    conn.commit();
    print("Table %s has been cleaned!" % TABLE_NAME);
    logger.info('表%s已被清空！',TABLE_NAME)

def import_data(cursor,ipaddress,app_name,app_code):
    global counter_dup
    sqlStr = "insert into {0} (WRITE_TIME,IP_ADDRESS,APP_NAME,APP_CODE) values (%s,%s,%s,%s)".format(TABLE_NAME)
    try:
        cursor.execute(sqlStr,(write_time,ipaddress,app_name,app_code));
    except:
        print('重复的记录:'+ ipaddress);
        logger.error('重复的记录: %s', ipaddress)
        counter_dup += 1

if __name__ == '__main__':
        main()
