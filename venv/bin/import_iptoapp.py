#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
from sub_common import *

# 设置log
logger = get_logger("import.log")

# 特定参数
conf = get_conf()
SOURCE_FILE = conf.get("SOURCE_FILE", "IPTOAPP_FILE")
TABLE_NAME = "ITM_IPTOAPP"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter_dup
global counter_err
global counter

def main():
    logger.info("Begin to import %s file!", SOURCE_FILE)
    global counter_err
    global counter
    counter_err = 0
    counter = 0

    delsql = "delete from {0} ".format(TABLE_NAME)
    clean_db(delsql);

    conn = get_conn()
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
                logger.error("Error record: %s",line)
                counter_err += 1

    conn.commit()
    conn.close()
    logger.info("Successfully import records:%s . Duplicated records:%s. Error records:%s",counter,counter_dup,counter_err)

def import_data(cursor,ipaddress,app_name,app_code):
    global counter_dup
    counter_dup = 0
    sqlStr = "insert into {0} (WRITE_TIME,IP_ADDRESS,APP_NAME,APP_CODE) values (%s,%s,%s,%s)".format(TABLE_NAME)
    try:
        cursor.execute(sqlStr,(write_time,ipaddress,app_name,app_code));
    except:
        print("Duplicated record:"+ ipaddress);
        logger.error("Duplicated record: %s", ipaddress)
        counter_dup += 1

if __name__ == '__main__':
        main()
