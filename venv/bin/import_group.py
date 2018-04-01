#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
from sub_common import *

# 设置log
logger = get_logger("import.log")

#文件示例： NT_TCP_STATUS_HT&&Primary:BL685762:NT Primary:BL685765:NT Primary:HP-BL685-019:NT Primary:HP-BL685-054:NT

# 特定参数
conf = get_conf()
SOURCE_FILE = conf.get("SOURCE_FILE", "GROUP_INFO")
TABLE_NAME = "ITM_GROUP_INFO"

# 设置全局变量
write_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
global counter

def main():
    logger.info("Begin to import %s file.",SOURCE_FILE)

    delsql = "delete from {0} ".format(TABLE_NAME)
    clean_db(delsql)

    process_group()

    logger.info("Import %s records.", counter)

def process_group():
    global counter
    counter = 0
    conn = get_conn()
    cursor = conn.cursor();
    with open(SOURCE_FILE, 'r',encoding='UTF-8') as file_to_read:
        for lines in file_to_read.readlines():
            lines_tmp =  lines.split('&&')
            groupname = lines_tmp[0]
            agent_all = lines_tmp[1].split()

            i = 0
            hostname = []
            while i <  len(agent_all):
                sqlStr = "insert into {0} (WRITE_TIME,GROUP_NAME,AGENT_NAME) values (%s,%s,%s)".format(TABLE_NAME)
                cursor.execute(sqlStr, (write_time, groupname, agent_all[i]));
                i = i + 1
                counter += 1
    conn.commit();
    conn.close();


if __name__ == '__main__':
        main()

