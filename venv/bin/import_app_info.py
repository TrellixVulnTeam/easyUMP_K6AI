#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.etree import ElementTree as et;
import datetime
from sub_common import *

# 设置log
logger = get_logger("import.log")

# 特定参数
conf = get_conf()
SROUCE_FILE = conf.get("SOURCE_FILE", "APP_INFO")
TABLE_NAME = "APP_INFO"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter

def main():
    logger.info("Begin to import %s file !", SROUCE_FILE)

    delsql = "delete from {0} ".format(TABLE_NAME)
    clean_db(delsql);

    process(SROUCE_FILE);

    logger.info("Total import %s records.",counter)


#处理XML文件
def process(APP_FILE):
    global counter
    counter = 0
    conn = get_conn()
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
        cursor.execute(sql)
        counter += 1
    conn.commit();
    conn.close()

if __name__ == '__main__':
    main()
