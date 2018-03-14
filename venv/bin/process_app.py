#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.etree import ElementTree as et;
import re
import logging
import pymysql


APP_FILE = "../src/sysInfo.xml"
TABLE_NAME = "itm_app_info"
LOG_FILE = "../logs/process_app.log"
MYSQL_SERVER = '192.168.3.155'
DB_USER = 'ump'
DB_PASS = '123456'
SCHEMA = 'ump'
global counter
counter = 0



#设置log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler(LOG_FILE)
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)


def main():
    clean_db();
    logger.info('开始导入从xml导入app数据！')
    process(APP_FILE);
    print("Total %s application have been imported !" % counter)
    logger.info('共导入完成%s条信息。',counter)


def clean_db():
    conn = pymysql.connect(MYSQL_SERVER,DB_USER,DB_PASS,SCHEMA,use_unicode=True, charset="utf8")
    cursor = conn.cursor();
    sql = "delete from " + TABLE_NAME
    cursor.execute(sql);
    conn.commit();
    print("Table %s has been cleaned!" % TABLE_NAME);
    logger.info('表%s已被清空！',TABLE_NAME)

def import_app(cursor,sql):
    global counter
    cursor.execute(sql);
    #print('insert data success');
    counter += 1

#处理XML文件
def process(APP_FILE):
    conn = pymysql.connect(MYSQL_SERVER,DB_USER,DB_PASS,SCHEMA,use_unicode=True,charset="utf8")
    cursor = conn.cursor();
    cursor.execute("set names utf8")
    root = et.parse(APP_FILE);
    for recordInfo in root.iter("recordInfo"):
        tempDict = recordInfo.attrib
        sql_tmp = "insert into {0} values(".format(TABLE_NAME);
        for fieldInfo in recordInfo.findall("fieldInfo"):
            slotName = fieldInfo.find('fieldChName').text;
            slotValue = fieldInfo.find("fieldContent").text;
            sql_tmp = sql_tmp + "'" + str(slotValue) + "',";
            tempDict[slotName] = slotValue;
        sql = sql_tmp[:-1];
        sql = sql + ");"
        import_app(cursor,sql);
    conn.commit();
    conn.close()

if __name__ == '__main__':
    main()
