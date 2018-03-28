#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import datetime
import sys
import logging
import pymysql
import os
import configparser

# 文件示例： 10.1.71.98	统一监控管理平台（UMP）	CEB-UMP

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
SOURCE_FILE = conf.get("SOURCE_FILE", "SIT_ENRICH_FILE")
LOG_FILE = conf.get("BASE_CONF", "LOG_PATH") + "/import_sit_enrich.log"
TABLE_NAME = "itm_sit_enrich"

#设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter
global counter_err
counter = 0
counter_err = 0

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
    process_sit_enrich()
    logger.info("Successfully import %s records!", counter)

def clean_db():
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    sql = "delete from " + TABLE_NAME
    cursor.execute(sql);
    conn.commit();
    print("Table %s has been cleaned!" % TABLE_NAME);
    logger.info("Table %s has been cleaned!",TABLE_NAME)

def process_sit_enrich():
    global  counter_err
    global  counter
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    with open(SOURCE_FILE, 'r',encoding='UTF-8') as file_to_read:
        for lines in file_to_read.readlines():
            lines_tmp =  lines.split('\t')

            SITNAME = lines_tmp[0]
            SIT_DESC = lines_tmp[1]
            THRESHOLD_FLAG = lines_tmp[2]
            CUR_VALUE_FLAG = lines_tmp[3]
            DISPLAY_FLAG = lines_tmp[4]
            N_ComponentType = lines_tmp[5]
            N_ComponentTypeId = lines_tmp[6]
            N_Component = lines_tmp[7]
            N_ComponentId = lines_tmp[8]
            N_SubComponent = lines_tmp[9]
            N_SubComponentId = lines_tmp[10]
            sqlStr = "insert into {0} (WRITE_TIME,SITNAME,SIT_DESC,THRESHOLD_FLAG,CUR_VALUE_FLAG,DISPLAY_FLAG,N_ComponentType,N_ComponentTypeId,N_Component,N_ComponentId,N_SubComponent,N_SubComponentId) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(TABLE_NAME)
            try:
                cursor.execute(sqlStr,(write_time,SITNAME,SIT_DESC,THRESHOLD_FLAG,CUR_VALUE_FLAG,DISPLAY_FLAG,N_ComponentType,N_ComponentTypeId,N_Component,N_ComponentId,N_SubComponent,N_SubComponentId));
                counter += 1
            except:
                    #print("Duplicated situation:%s" % SITNAME)
                    logger.error("Duplicated situation: %s", SITNAME )
                    counter_err += 1
    conn.commit()
    conn.close()

if __name__ == '__main__':
        main()

