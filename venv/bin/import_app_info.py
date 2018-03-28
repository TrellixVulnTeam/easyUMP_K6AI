#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.etree import ElementTree as et;
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
SROUCE_FILE = conf.get("SOURCE_FILE", "APP_INFO")
LOG_FILE = conf.get("BASE_CONF", "LOG_PATH") + "/import_app_info.log"
TABLE_NAME = "app_info"

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
    clean_db();
    logger.info("Begin to import %s file !",SROUCE_FILE)
    process(SROUCE_FILE);
    print("Total %s application have been imported !" % counter)
    logger.info("Total import %s records.",counter)


def clean_db():
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    sql = "delete from " + TABLE_NAME
    cursor.execute(sql);
    conn.commit();
    conn.close()
    print("Table %s has been cleaned!" % TABLE_NAME);
    logger.info('Table %s has been cleaned!',TABLE_NAME)

def import_app(cursor,sql):
    global counter
    cursor.execute(sql);
    #print('insert data success');
    counter += 1

#处理XML文件
def process(APP_FILE):
    conn = pymysql.connect(host=DB_IP,port=int(DB_PORT),user=DB_USER,passwd=DB_PASSWORD,db=DB_SCHEMA,use_unicode=True,charset=DB_CHARSET)
    cursor = conn.cursor();
    cursor.execute("set names utf8")
    root = et.parse(APP_FILE);
    for recordInfo in root.iter("recordInfo"):
        tempDict = recordInfo.attrib
        sql_tmp = "insert into {0} values('{1}',".format(TABLE_NAME,write_time);
        for fieldInfo in recordInfo.findall("fieldInfo"):
            slotName = fieldInfo.find('fieldChName').text;
            slotValue = fieldInfo.find("fieldContent").text;
            if (slotName == '系统上线时间' or slotName == '系统下线时间') and not slotValue:
                slotValue = 0
            sql_tmp = sql_tmp + "'" + str(slotValue) + "',";
            tempDict[slotName] = slotValue;
        sql = sql_tmp[:-1];
        sql = sql + ");"
        import_app(cursor,sql);
    conn.commit();
    conn.close()

if __name__ == '__main__':
    main()
